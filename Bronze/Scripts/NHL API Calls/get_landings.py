from pathlib import Path
import os

# These are the years in which each season started (i.e., 2021 = 2021-22 season)
seasons = ['2021', '2022', '2023', '2024', '2025']

p = Path('../../Data/Landings')
if not p.exists():
    p.mkdir()
    for season in seasons:
        p = Path(f'../../Data/Landings/{season}')
        print(f'Creating folder: {p}')
        p.mkdir()

game_type = '02' # Regular season
for season in seasons:
    for game_number in range(1, 1313):
        game_number_padded = str(game_number).zfill(4)
        game_id = f'{season}{game_type}{game_number_padded}'
        landing_path = f'../../Data/Landings/{season}/{game_id}.json'
        p = Path(landing_path)
        if not p.exists(): # Check to see if json already retrieved, for reentrancy
            print(f'Retrieving {game_id}.')
            os.system(f'curl -X GET "https://api-web.nhle.com/v1/gamecenter/{game_id}/landing" | python3 -m json.tool > "{landing_path}"')
        else:
            print(f'Already retrieved {game_id}.')