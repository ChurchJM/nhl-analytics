import sys
from pathlib import Path
import json
import pandas as pd

sweaters_path = '../../Data/Tables/sweaters.csv' 
p = Path(sweaters_path)
if not p.exists():
    print('Sweaters table must be built first via the Silver/Scripts/Build Tables/sweaters.py script.')
    sys.exit(1)

df_sweaters = pd.read_csv(sweaters_path)
df_sweaters['effective_date'] = pd.to_datetime(df_sweaters['effective_date'])

p = Path('../../../Bronze/Data/Landings')
if not p.exists():
    print('Landings must be downloaded first via the Bronze/Scripts/NHL API Calls/get_landings.py script.')
    sys.exit(1)

SECONDS_IN_PERIOD = pd.to_timedelta('00:20:00').seconds

def get_sweater_id(player_id, game_date):
    # Get most recent sweater with effective_date prior or equal to the game_date (e.g., the current sweater as of the game)
    # This relies on df_sweaters being sorted by effective_date, which is done in sweaters.py    
    return df_sweaters[(df_sweaters['player_id']==player_id)&(df_sweaters['effective_date']<=pd.to_datetime(game_date))].iloc[-1, 0]     

goal_id = 1
goal_rows = []
assist_rows = []

for landing_path in p.rglob('*.json'):
    with open(landing_path, 'r') as f:
        data = json.load(f)
        game_id = data['id']
        game_date = data['gameDate']
        for period in range(len(data['summary']['scoring'])):
            period_goals = data['summary']['scoring'][period]['goals']
            for goal in period_goals:
                player_id = goal['playerId']
                sweater_id = get_sweater_id(player_id, game_date)
                goal_strength = goal['strength']

                # Denote shootout goals (e.g., period 4) as -1 seconds
                if period < 4:
                    seconds_into_game = (period * SECONDS_IN_PERIOD) + pd.to_timedelta(f"{00}:{goal['timeInPeriod']}").seconds
                else:
                    seconds_into_game = -1

                goal_rows.append([goal_id, game_id, sweater_id, goal_strength, seconds_into_game])
                
                for assist in goal['assists']:
                    player_id = assist['playerId']
                    sweater_id = get_sweater_id(player_id, game_date)
                    assist_rows.append([goal_id, sweater_id]) # ToDo: Add first/second assist?

                goal_id += 1

df_goals = pd.DataFrame(goal_rows, columns=['id', 'game_id', 'sweater_id', 'goal_strength', 'seconds_in'])
# print(df_goals.sort_values(by=['game_id', 'seconds_in']).head(10))

df_assists = pd.DataFrame(assist_rows, columns=['goal_id', 'sweater_id']).reset_index()
df_assists.rename(columns={'index' : 'id'}, inplace=True)
df_assists['id'] = df_assists['id']+1

print(df_assists.sort_values(by='goal_id').head(20))

# df_goals.to_csv('../../Data/Tables/goals.csv', index=False)
# df_assists.to_csv('../../Data/Tables/assists.csv', index=False)