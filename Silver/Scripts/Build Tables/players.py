import sys
from pathlib import Path
import json
import pandas as pd

p = Path('../../../Bronze/Data/Player Info')
if not p.exists():
    print('Player info must be downloaded first via the Bronze/Scripts/NHL API Calls/get_player_info.py script.')
    sys.exit(1)

player_rows = []

p = Path(f'../../../Bronze/Data/Player Info')
for box_score_path in p.rglob('*.json'):
    with open(box_score_path, 'r') as f:
        data = json.load(f)
        player_rows.append([
            data['playerId'],
            data['firstName']['default'],
            data['lastName']['default'],
            data['birthCountry'],
            data['birthDate']
            ])

df_players = pd.DataFrame(player_rows, columns=['id', 'first', 'last', 'nationality', 'birth_date'])

# Need to add dummy rows for each team so that we have a "player" to serve bench minors.
team_dummy_rows = [
    [-1, 'New Jersey', 'Devils', 'USA', '1974-01-01'],
    [-2, 'New York', 'Islanders', 'USA', '1972-01-01'],
    [-3, 'New York', 'Rangers', 'USA', '1926-01-01'],
    [-4, 'Philadelphia', 'Flyers', 'USA', '1967-01-01'],
    [-5, 'Pittsburgh', 'Penguins', 'USA', '1967-01-01'],
    [-6, 'Boston', 'Bruins', 'USA', '1924-01-01'],
    [-7, 'Buffalo', 'Sabres', 'USA', '1970-01-01'],
    [-8, 'Montreal', 'Canadiens', 'CAN', '1909-01-01'],
    [-9, 'Ottawa', 'Senators', 'CAN', '1992-01-01'],
    [-10, 'Toronto', 'Maple Leafs', 'CAN', '1917-01-01'],
    [-12, 'Carolina', 'Hurricanes', 'USA', '1972-01-01'],
    [-13, 'Florida', 'Panthers', 'USA', '1993-01-01'],
    [-14, 'Tampa Bay', 'Lightning', 'USA', '1990-01-01'],
    [-15, 'Washington', 'Capitals', 'USA', '1974-01-01'],
    [-16, 'Chicago', 'Blackhawks', 'USA', '1926-01-01'],
    [-17, 'Detroit', 'Red Wings', 'USA', '1926-01-01'],
    [-18, 'Nashville', 'Predators', 'USA', '1998-01-01'],
    [-19, 'St. Louis', 'Blues', 'USA', '1967-01-01'],
    [-20, 'Calgary', 'Flames', 'CAN', '1972-01-01'],
    [-21, 'Colorado', 'Avalanche', 'USA', '1972-01-01'],
    [-22, 'Edmonton', 'Oilers', 'CAN', '1972-01-01'],
    [-23, 'Vancouver', 'Canucks', 'CAN', '1970-01-01'],
    [-24, 'Anaheim', 'Ducks', 'USA', '1993-01-01'],
    [-25, 'Dallas', 'Stars', 'USA', '1967-01-01'],
    [-26, 'Los Angeles', 'Kings', 'USA', '1967-01-01'],
    [-28, 'San Jose', 'Sharks', 'USA', '1990-01-01'],
    [-29, 'Columbus', 'Blue Jackets', 'USA', '1997-01-01'],
    [-30, 'Minnesota', 'Wild', 'USA', '1997-01-01'],
    [-52, 'Winnipeg', 'Jets', 'CAN', '1997-01-01'],
    [-53, 'Arizona', 'Coyotes', 'USA', '1971-01-01'],
    [-54, 'Vegas', 'Golden Knights', 'USA', '2016-01-01'],
    [-55, 'Seattle', 'Kraken', 'USA', '2021-01-01'],
    [-68, 'Utah', 'Mammoth', 'USA', '2024-01-01']
]

df_team_dummies = pd.DataFrame(team_dummy_rows, columns=['id', 'first', 'last', 'nationality', 'birth_date'])
df_players = pd.concat([df_players, df_team_dummies])
df_players = df_players.sort_values(by='id').reset_index(drop=True)

# print(df_players.head(10000))

df_players.to_csv('../../Data/Tables/players.csv', index=False)