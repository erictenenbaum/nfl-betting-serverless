import uuid

# game_data function takes in csv row and nfl teams list to create game objects with these fields:
def game_data(row, nfl_teams):
    return {
        '_id': str(uuid.uuid4()),
        'stadium': row['stadium'],
        'season': int(row['schedule_season']),
        'week': row['schedule_week'],
        'playoff_game': False if row['schedule_playoff'] == 'FALSE' else True,
        'home_team': {
            'team_id': team_to_id_converter(row['team_home'], nfl_teams=nfl_teams),
            'team': row['team_home'],
            'favored': team_to_id_converter(row['team_home'], nfl_teams=nfl_teams) == row['team_favorite_id'],
            'points_scored': int(row['score_home'])
        },
        'away_team': {
            'team_id': team_to_id_converter(row['team_away'], nfl_teams=nfl_teams),
            'team': row['team_away'],
            'favored': team_to_id_converter(row['team_away'], nfl_teams) == row['team_favorite_id'],
            'points_scored': int(row['score_away'])
        },
        'betting': {
            'spread': {
                'points': 'PICK' if row['spread_favorite'] == 'PICK' else float(row['spread_favorite']),
                'covered': calculate_spread(row=row, nfl_teams=nfl_teams)
            },
            'over_under': {
                'points': row['over_under_line'] if len(row['over_under_line']) > 0 else 'N/A',
                'covered': calculate_over_under(row=row) if len(row['over_under_line'].strip()) > 0 else None
            }
        }
    }


# function that takes in a team name (teams have changed names over the years) and returns the 'TV code' you see in broadcasts
def team_to_id_converter(team_name, nfl_teams):
    for team in nfl_teams:
        if team_name in team['full_name']:
            return team['code']
    return None


# function that returns true if the favored team covers, false if the underdog covers, and None/null if its a push
def calculate_spread(row, nfl_teams):
    if row['spread_favorite'] == 'PICK':
        return None
    spread = float(row['spread_favorite'])
    home_points = float(row['score_home'])
    away_points = float(row['score_away'])
    home_team_favored = team_to_id_converter(row['team_home'], nfl_teams=nfl_teams) == row['team_favorite_id']

    if home_team_favored:
        return None if (home_points - spread) == away_points else (home_points - spread) > away_points

    return None if (away_points - spread) == home_points else (away_points - spread) > home_points


# returns true if the over hits, false if the under hits and None/null if its a push
def calculate_over_under(row):
    combined_score = (float(row['score_home']) + float(row['score_away']))
    line = float(row['over_under_line'])
    return None if combined_score == line else combined_score > line