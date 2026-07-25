import sys
from pathlib import Path
import pandas as pd

game_ref_mapping_path = '../../Data/Raw/game_ref_mapping.csv'
p = Path(game_ref_mapping_path)
if not p.exists():
    print('Game ref mapping must be built first via the Silver/Scripts/Data Cleaning/clean_referees.ipynb notebook.')
    sys.exit(1)

df_game_ref = pd.read_csv(game_ref_mapping_path)

penalties_path = '../../Data/Tables/penalties.csv'
p = Path(penalties_path)
if not p.exists():
    print('Penalties table must be built first via the Silver/Scripts/Build Tables/penalties.py script.')
    sys.exit(1)

df_penalties = pd.read_csv(penalties_path)

df_calls = pd.merge(df_penalties, df_game_ref, how='left', on='game_id')
df_calls = df_calls[['id', 'referee_id']]
df_calls = df_calls.reset_index().rename(columns={'id' : 'penalty_id', 'index' : 'id'})
df_calls['id'] = df_calls['id']+1

# print(df_calls.head(20))

df_calls.to_csv('../../Data/Tables/calls.csv', index=False)