import sys
from pathlib import Path
import json
import pandas as pd

teams_path = '../../Data/Tables/teams.csv'
p = Path(teams_path)
if not p.exists():
    print('Teams table must be built first via the Silver/Scripts/Build Tables/teams.py script.')
    sys.exit(1)

df_teams = pd.read_csv(teams_path)

p = Path('../../../Bronze/Data/Landings')
if not p.exists():
    print('Landings must be downloaded first via the Bronze/Scripts/NHL API Calls/get_landings.py script.')
    sys.exit(1)

game_rows = []

for landing_path in p.rglob('*.json'):
    with open(landing_path, 'r') as f:
        data = json.load(f)
        game_id = data['id']
        game_date = data['gameDate']
        season = data['season']
        game_type = 2 # regular season
        game_number = int(str(game_id)[-4:])
        home_team_id = df_teams[df_teams['abbreviation']==data['homeTeam']['abbrev']].iloc[0,0]
        away_team_id = df_teams[df_teams['abbreviation']==data['awayTeam']['abbrev']].iloc[0,0]

        game_rows.append([game_id, home_team_id, away_team_id, season, game_type, game_number, game_date])

df_games = pd.DataFrame(game_rows, columns=['id', 'home_team_id', 'away_team_id', 'season', 'game_type', 'game_number', 'game_date'])

# print(df_games.head())

df_games.to_csv('../../Data/Tables/games.csv', index=False)