from pathlib import Path
import json
import os

p = Path('../../Data/Player Info')
if not p.exists():
    p.mkdir()

player_ids = []

box_scores_root = Path('../../Data/Box Scores')
for box_score_path in box_scores_root.rglob('*.json'):
    with open(box_score_path, 'r') as f:
        data = json.load(f)
        homePlayers = data['playerByGameStats']['homeTeam']
        awayPlayers = data['playerByGameStats']['awayTeam']
        positions = ['forwards', 'defense', 'goalies']
        for position in positions:
            for player in homePlayers[position]:
                player_id = player['playerId']
                if player_id not in player_ids:
                    player_ids.append(player_id)
            for player in awayPlayers[position]:
                player_id = player['playerId']
                if player_id not in player_ids:
                    player_ids.append(player_id)

for player_id in player_ids:
    player_info_path = f'../../Data/Player Info/{player_id}.json'
    p = Path(player_info_path)
    if not p.exists(): # Check to see if json already retrieved, for reentrancy
        print(f'Retrieving {player_id}.')
        os.system(f'curl -X GET "https://api-web.nhle.com/v1/player/{player_id}/landing" | python3 -m json.tool > "{player_info_path}"')
    else:
        print(f'Already retrieved {player_id}.')