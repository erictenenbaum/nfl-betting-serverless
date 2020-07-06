# updates stats for home and a way teams in the list and then returns the list
def update_nfl_team_data(game, nfl_teams):
    nfl_teams[find_team_index(game['home_team'], nfl_teams)] = update_team(game, game['home_team'], nfl_teams)
    nfl_teams[find_team_index(game['away_team'], nfl_teams)] = update_team(game, game['away_team'], nfl_teams)
    return nfl_teams


# finds index in nfl_teams list that corresponds to the team passed in
def find_team_index(current_team, nfl_teams):
    for index, team in enumerate(nfl_teams):
        if current_team['team_id'] == team['code']:
            return index


# function that updates team stats for every individual games (that has betting data)
def update_team(game, team, nfl_teams):
    team_index = find_team_index(current_team=team, nfl_teams=nfl_teams)
    is_home_team = team['team_id'] == game['home_team']['team_id']
    is_won_game = None

    if is_home_team:
        if game['home_team']['points_scored'] > game['away_team']['points_scored']:
            is_won_game = True
        else:
            is_won_game = False

    if not is_home_team:
        if game['away_team']['points_scored'] > game['home_team']['points_scored']:
            is_won_game = True
        else:
            is_won_game = False

    if 'stats' not in nfl_teams[team_index]:
        nfl_teams[team_index]['stats'] = {
            'total_wins': 0,
            'playoff_wins': 0,
            'betting': {
                'spread': {
                    'covered': {
                        'count': 0,
                        'games': []
                    },
                    'did_not_cover': {
                        'count': 0,
                        'games': []
                    },
                    'push': {
                        'count': 0,
                        'games': []
                    }
                },
                'over_under': {
                    'covered': {
                        'count': 0,
                        'games': []
                    },
                    'did_not_cover': {
                        'count': 0,
                        'games': []
                    },
                    'push': {
                        'count': 0,
                        'games': []
                    }
                }
            }
        }

    if is_won_game:
        nfl_teams[team_index]['stats']['total_wins'] = nfl_teams[team_index]['stats']['total_wins'] + 1
        nfl_teams[team_index]['stats']['playoff_wins'] = nfl_teams[team_index]['stats']['playoff_wins'] + 1 if game[
            'playoff_game'] else nfl_teams[team_index]['stats']['playoff_wins']

    return over_under_update(game=game, team_index=team_index,
                             nfl_teams=point_spread_update(game=game, team=team, is_won_game=is_won_game,
                                                           team_index=team_index, nfl_teams=nfl_teams))[team_index]


# function that updates the over_under stats for team in nfl_teams array
def over_under_update(game, team_index, nfl_teams):
    if game['betting']['over_under']['points'] != 'N/A':

        # if the over covered, increment covered counter and add game id to the list of covered games
        if game['betting']['over_under']['covered']:
            nfl_teams[team_index]['stats']['betting']['over_under']['covered']['count'] = \
                nfl_teams[team_index]['stats']['betting']['over_under']['covered']['count'] + 1
            nfl_teams[team_index]['stats']['betting']['over_under']['covered']['games'].append(game['_id'])

        # if covered is a None/null value increment push counter and add game id to the list of push games
        elif game['betting']['over_under']['covered'] is None:
            nfl_teams[team_index]['stats']['betting']['over_under']['push']['count'] = \
                nfl_teams[team_index]['stats']['betting']['over_under']['push']['count'] + 1
            nfl_teams[team_index]['stats']['betting']['over_under']['push']['games'].append(game['_id'])

        # if the over wasn't covered and it wasn't a push, then the over didn't hit: update stats accordingly
        else:
            nfl_teams[team_index]['stats']['betting']['over_under']['did_not_cover']['count'] = \
                nfl_teams[team_index]['stats']['betting']['over_under']['did_not_cover']['count'] + 1
            nfl_teams[team_index]['stats']['betting']['over_under']['did_not_cover']['games'].append(game['_id'])

    return nfl_teams


# function that
def point_spread_update(game, team, is_won_game, team_index, nfl_teams):
    # if game is a "pickem" increment covered and add game to list for the winning team
    if game['betting']['spread']['points'] == 'PICK':
        if is_won_game:
            nfl_teams[team_index]['stats']['betting']['spread']['covered']['count'] = \
                nfl_teams[team_index]['stats']['betting']['spread']['covered']['count'] + 1
            nfl_teams[team_index]['stats']['betting']['spread']['covered']['games'].append(game['_id'])
        else:
            nfl_teams[team_index]['stats']['betting']['spread']['did_not_cover']['count'] = \
                nfl_teams[team_index]['stats']['betting']['spread']['did_not_cover']['count'] + 1
            nfl_teams[team_index]['stats']['betting']['spread']['did_not_cover']['games'].append(game['_id'])

    # if team was favored and the spread was covered or team was not favored and spread was not covered, update the team's covered stats:
    if (team['favored'] and game['betting']['spread']['covered']) or (
            not team['favored'] and not game['betting']['spread']['covered'] and game['betting']['spread']
        ['covered'] is not None):
        nfl_teams[team_index]['stats']['betting']['spread']['covered']['count'] = \
            nfl_teams[team_index]['stats']['betting']['spread']['covered']['count'] + 1
        nfl_teams[team_index]['stats']['betting']['spread']['covered']['games'].append(game['_id'])
    else:
        nfl_teams[team_index]['stats']['betting']['spread']['did_not_cover']['count'] = \
            nfl_teams[team_index]['stats']['betting']['spread']['did_not_cover']['count'] + 1
        nfl_teams[team_index]['stats']['betting']['spread']['did_not_cover']['games'].append(game['_id'])

    # if covered is None/null game was a push
    if game['betting']['spread']['covered'] is None:
        nfl_teams[team_index]['stats']['betting']['spread']['push']['count'] = \
            nfl_teams[team_index]['stats']['betting']['spread']['push']['count'] + 1
        nfl_teams[team_index]['stats']['betting']['spread']['push']['games'].append(game['_id'])

    return nfl_teams
