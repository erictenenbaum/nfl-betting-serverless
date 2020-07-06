import json
import csv
import boto3
import os
import uuid

from create_game_data import game_data
from update_team_data import update_nfl_team_data

s3 = boto3.client('s3', aws_access_key_id=os.getenv('ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY')) 


def cleanse_data(event, context):
    # retrieve nfl_teams.json from S3
    s3_nfl_teams_obj = s3.get_object(Bucket=os.getenv('BUCKET_NAME'), Key='nfl_teams.json')
    s3_nfl_teams_data = s3_nfl_teams_obj['Body'].read().decode('utf-8')
    nfl_teams = json.loads(s3_nfl_teams_data)

    # retrieve nfl game data csv file from S3
    s3_games_obj = s3.get_object(Bucket=os.getenv('BUCKET_NAME'), Key='data-csv.csv')
    s3_games_data = s3_games_obj['Body'].read().decode('utf-8').splitlines(True)

    # iterate through csv game data and run games with point spread betting data through data cleansing/data prep functions
    clean_data = list()  
    data = csv.DictReader(s3_games_data)
    for row in data:
        if len(row['spread_favorite'].strip()) > 0 or len(row['spread_favorite'].strip()):
            game = game_data(row=row, nfl_teams=nfl_teams)
            nfl_teams = update_nfl_team_data(game=game, nfl_teams=nfl_teams)
            clean_data.append(game)

    # after cleaning and prepping the data, upload json files to a clean-data path in S3 to trigger another lambda to upload data into DynamoDB
    nfl_teams = list(map(lambda team: add_uuid(team), nfl_teams))
    s3.put_object(Body=json.dumps({"DynamoDB_Table": "Teams", "data": nfl_teams}), Bucket=os.getenv('BUCKET_NAME'), Key='clean-data/nfl_teams.json')
    s3.put_object(Body=json.dumps(
        {
            "DynamoDB_Table": "Games",
            "data": list(map(lambda game_obj: convert_floats_to_strings(game_obj), clean_data))
        }), Bucket=os.getenv('BUCKET_NAME'), Key='clean-data/games.json')
    return json.dumps(
        {
            "statusCode": 200,
            "body": {
                "message": "success"
            }
        }
    )


# add a unique id to nfl_teams data
def add_uuid(doc):
    doc['_id'] = str(uuid.uuid4())
    return doc


# ran into a weird issue where DynamoDB doesn't play nice with python floats, so convert these float values to strings. If I need to work with the data
# elsewhere, I'll need to parse them back into floats.
def convert_floats_to_strings(game_data_dict):
    game_data_dict['betting']['spread']['points'] = str(game_data_dict['betting']['spread']['points'])
    game_data_dict['betting']['over_under']['points'] = str(game_data_dict['betting']['over_under']['points'])
    return game_data_dict


