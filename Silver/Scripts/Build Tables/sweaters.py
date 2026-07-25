import sys
from pathlib import Path
import json
import pandas as pd

p = Path('../../../Bronze/Data/Box Scores')
if not p.exists():
    print('Box scores must be downloaded first via the Bronze/Scripts/NHL API Calls/get_box_scores.py script.')
    sys.exit(1)

sweater_rows = []

for box_score_path in p.rglob('*.json'):
    with open(box_score_path, 'r') as f:
        data = json.load(f)
        date = data['gameDate']
        home_team_id = data['homeTeam']['id']
        away_team_id = data['awayTeam']['id']
        homePlayers = data['playerByGameStats']['homeTeam']
        awayPlayers = data['playerByGameStats']['awayTeam']
        positions = ['forwards', 'defense', 'goalies']
        for position in positions:
            pos_abbrev = position[0].upper()
            for player in homePlayers[position]:
                sweater_rows.append([player['playerId'], home_team_id, player['sweaterNumber'], pos_abbrev, date])
            for player in awayPlayers[position]:
                sweater_rows.append([player['playerId'], away_team_id, player['sweaterNumber'], pos_abbrev, date])

df_sweaters = pd.DataFrame(sweater_rows, columns=['player_id', 'team_id', 'number', 'position', 'effective_date'])

# Need to add dummy rows for each team so that we have a "player" to serve bench minors.
team_dummy_rows = [
    [-1, 1, 0, 'T', '1974-01-01'],
    [-2, 2, 0, 'T', '1972-01-01'],
    [-3, 3, 0, 'T', '1926-01-01'],
    [-4, 4, 0, 'T', '1967-01-01'],
    [-5, 5, 0, 'T', '1967-01-01'],
    [-6, 6, 0, 'T', '1924-01-01'],
    [-7, 7, 0, 'T', '1970-01-01'],
    [-8, 8, 0, 'T', '1909-01-01'],
    [-9, 9, 0, 'T', '1992-01-01'],
    [-10, 10, 0, 'T', '1917-01-01'],
    [-12, 12, 0, 'T', '1972-01-01'],
    [-13, 13, 0, 'T', '1993-01-01'],
    [-14, 14, 0, 'T', '1990-01-01'],
    [-15, 15, 0, 'T', '1974-01-01'],
    [-16, 16, 0, 'T', '1926-01-01'],
    [-17, 17, 0, 'T', '1926-01-01'],
    [-18, 18, 0, 'T', '1998-01-01'],
    [-19, 19, 0, 'T', '1967-01-01'],
    [-20, 20, 0, 'T', '1972-01-01'],
    [-21, 21, 0, 'T', '1972-01-01'],
    [-22, 22, 0, 'T', '1972-01-01'],
    [-23, 23, 0, 'T', '1970-01-01'],
    [-24, 24, 0, 'T', '1993-01-01'],
    [-25, 25, 0, 'T', '1967-01-01'],
    [-26, 26, 0, 'T', '1967-01-01'],
    [-28, 28, 0, 'T', '1990-01-01'],
    [-29, 29, 0, 'T', '1997-01-01'],
    [-30, 30, 0, 'T', '1997-01-01'],
    [-52, 52, 0, 'T', '1997-01-01'],
    [-53, 53, 0, 'T', '1971-01-01'],
    [-54, 54, 0, 'T', '2016-01-01'],
    [-55, 55, 0, 'T', '2021-01-01'],
    [-68, 68, 0, 'T', '2024-01-01']
]

df_team_dummies = pd.DataFrame(team_dummy_rows, columns=['player_id', 'team_id', 'number', 'position', 'effective_date'])
df_sweaters = pd.concat([df_sweaters, df_team_dummies])

df_sweaters['effective_date'] = pd.to_datetime(df_sweaters['effective_date'])
df_sweaters = df_sweaters.sort_values(by=['player_id', 'effective_date']).drop_duplicates(subset=['player_id', 'team_id', 'number', 'position'], keep='first')
df_sweaters.reset_index(inplace=True, drop=True) # original ordering is meaningless
df_sweaters.reset_index(inplace=True) # add id column with meaningful ordering
df_sweaters.rename(columns={'index':'id'}, inplace=True)
df_sweaters['id'] = df_sweaters.apply(lambda row: -row['team_id'] if row['id']<33 else row['id']-32, axis=1)

# Vladimir Tarasenko, an example of a player who was traded a lot
# print(df_sweaters[df_sweaters['player_id']==8475765].head(100))

# What players played multiple positions in 2021-2025 seasons?
# Looks like just two: Kurtis MacDermid (8477073) and Mason Geertsen (8477419)
# df_changed_pos = df_sweaters.groupby('player_id').filter(lambda x: x['position'].nunique() > 1)
# print(df_changed_pos.sort_values(by=['player_id','effective_date']).head(100))

# print(df_sweaters.head(20))

df_sweaters.to_csv('../../Data/Tables/sweaters.csv', index=False)