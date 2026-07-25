from pathlib import Path
import os

seasons = ['20212022', '20222023', '20232024', '20242025', '20252026']

p = Path('../../Data/HTML Game Summaries')
if not p.exists():
    p.mkdir()
    for season in seasons:
        p = Path(f'../../Data/HTML Game Summaries/{season}')
        print(f'Creating folder: {p}')
        p.mkdir()

game_type = '02' # Regular season
for season in seasons:
    for game_number in range(1, 1313):
        game_number_padded = str(game_number).zfill(4)
        game_id = f'{season}{game_type}{game_number_padded}'
        summary_path = f'../../Data/HTML Game Summaries/{season}/{game_id}.HTM'
        p = Path(summary_path)
        if not p.exists(): # Check to see if json already retrieved, for reentrancy
            print(f'Retrieving {game_id}.')
            os.system(f'curl -X GET "https://www.nhl.com/scores/htmlreports/{season}/GS{game_type}{game_number_padded}.HTM" > "{summary_path}"')
        else:
            print(f'Already retrieved {game_id}.')