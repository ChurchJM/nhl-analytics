import sys
from pathlib import Path
import json
import pandas as pd
import unicodedata

teams_path = '../../Data/Tables/teams.csv'
p = Path(teams_path)
if not p.exists():
    print('Teams table must be built first via the Silver/Scripts/Build Tables/teams.py script.')
    sys.exit(1)

df_teams = pd.read_csv(teams_path)

sweaters_path = '../../Data/Tables/sweaters.csv' 
p = Path(sweaters_path)
if not p.exists():
    print('Sweaters table must be built first via the Silver/Scripts/Build Tables/sweaters.py script.')
    sys.exit(1)

df_sweaters = pd.read_csv(sweaters_path)
df_sweaters['effective_date'] = pd.to_datetime(df_sweaters['effective_date'])

penalty_types_path = '../../Data/Tables/penalty_types.csv'
p = Path(penalty_types_path)
if not p.exists():
    print('Penalty Types table must be built first via the Silver/Scripts/Build Tables/penalty_types.py script.')
    sys.exit(1)

df_penalty_types = pd.read_csv(penalty_types_path)

p = Path('../../../Bronze/Data/Box Scores')
if not p.exists():
    print('Box scores must be downloaded first via the Bronze/Scripts/NHL API Calls/get_box_scores.py script.')
    sys.exit(1)

p = Path('../../../Bronze/Data/Landings')
if not p.exists():
    print('Landings must be downloaded first via the Bronze/Scripts/NHL API Calls/get_landings.py script.')
    sys.exit(1)

SECONDS_IN_PERIOD = pd.to_timedelta('00:20:00').seconds

def remove_accents(name):
    # Decompose characters into base letters and accent modifiers
    nfkd_form = unicodedata.normalize('NFKD', name)
    # Filter out characters that are classified as combining marks (diacritics)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

# Landings do not include player_ids of penalty takers. Need to lookup player_ids in corresponding box scores.
def get_player_id(game_id, offender):
    matching_player_ids = []
    offender_first_initial = remove_accents(offender['firstName']['default'])[0].upper()
    offender_last = remove_accents(offender['lastName']['default']).upper()
    offender_number = offender['sweaterNumber']
    with open(f'../../../Bronze/Data/Box Scores/{str(game_id)[:4]}/{game_id}.json') as f:
        data = json.load(f)
        home_players = data['playerByGameStats']['homeTeam']
        away_players = data['playerByGameStats']['awayTeam']
        positions = ['forwards', 'defense', 'goalies']
        players = []
        for position in positions:
            players = players + home_players[position]
            players = players + away_players[position]
        for player in players:
            player_name = remove_accents(player['name']['default'])
            dot_idx = player_name.find('.')
            player_first_initial = player_name[:dot_idx].strip().upper()
            player_last = player_name[dot_idx+1:].strip().upper()                            
            player_number = player['sweaterNumber']
            if (player_first_initial == offender_first_initial
                and player_last == offender_last
                and player_number == offender_number):
                    matching_player_ids.append(player['playerId'])
    
    if len(matching_player_ids) != 1:
         print('Multiple or zero matches!', game_id, offender_first_initial, offender_last)
         sys.exit(1)
    
    return matching_player_ids[0]
    
def get_sweater_id(player_id, game_date):
    # Get most recent sweater with effective_date prior or equal to the game_date (e.g., the current sweater as of the game)
    # This relies on df_sweaters being sorted by effective_date, which is done in sweaters.py    
    return df_sweaters[(df_sweaters['player_id']==player_id)&(df_sweaters['effective_date']<=pd.to_datetime(game_date))].iloc[-1, 0]

SECONDS_IN_PERIOD = pd.to_timedelta('00:20:00').seconds

penalty_rows = []

for landing_path in p.rglob('*.json'):
    with open(landing_path, 'r') as f:
        data = json.load(f)
        game_id = data['id']
        game_date = data['gameDate']
        for period in range(3):
            period_penalties = data['summary']['penalties'][period]['penalties']
            for penalty in period_penalties:
                # ------------------------- GET SWEATER ID -------------------------
                if 'committedByPlayer' in penalty:
                    offender = penalty['committedByPlayer']
                    offender_id = get_player_id(game_id, offender)
                    sweater_id = get_sweater_id(offender_id, game_date)
                else: # Bench minor; need to assign penalty to dummy team sweater
                    offender_team = penalty['teamAbbrev']['default']
                    sweater_id = df_teams[df_teams['abbreviation']==offender_team].iloc[0,0]*(-1) # dummy rows have negative ids

                # ------------------------ GET PENALTY TYPE ID -----------------------
                penalty_type = penalty['descKey']
                penalty_type_id = df_penalty_types[df_penalty_types['name']==penalty_type].iloc[0,0]

                # ------------------------ CALCULATE SECONDS IN ----------------------
                if period < 4:
                    seconds_into_game = (period * SECONDS_IN_PERIOD) + pd.to_timedelta(f"{00}:{penalty['timeInPeriod']}").seconds
                else:
                    seconds_into_game = -1 # Can penalties be called during the shootout?
                
                penalty_rows.append([game_id, sweater_id, penalty_type_id, seconds_into_game])

df_penalties = pd.DataFrame(penalty_rows, columns=['game_id', 'sweater_id', 'penalty_type_id', 'seconds_in']).sort_values(by='game_id')
df_penalties = df_penalties.reset_index(drop=True).reset_index()
df_penalties.rename(columns={'index': 'id'}, inplace=True)
df_penalties['id'] = df_penalties['id']+1

# print(df_penalties.head(20))

df_penalties.to_csv('../../Data/Tables/penalties.csv', index=False)



                

                
                
                
                    
