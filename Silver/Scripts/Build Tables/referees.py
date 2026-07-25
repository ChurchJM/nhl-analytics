import sys
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd

p = Path('../../../Bronze/Data/HTML Game Summaries')
if not p.exists():
    print('Player info must be downloaded first via the Bronze/Scripts/NHL API Calls/get_player_info.py script.')
    sys.exit(1)

referee_rows = []

for summary_path in p.rglob('*.HTM'):
    with open(summary_path, 'r') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        
        game_id = str(summary_path)[-18:-14] + str(summary_path)[-10:-4]

        all_tables = soup.find(id='MainTable').find_all('table')
        for table in all_tables:
            child_tables = table.find_all('table')
            if 'Referee' in table.text:
                referee_table = child_tables[0]
                linesmen_table = child_tables[1]
                referee_standby_table = child_tables[2]
                linesmen_standby_table = child_tables[3]
        
        referees = referee_table.text.strip().split('\n')
        referees = [referee for referee in referees if len(referee) != 0]
        referee_1 = referees[0]
        
        if len(referees) == 2:
            referee_2 = referees[1]
        else:
            referee_2 = '' # Check for this in next stage (compile_referees.py), might be present in standby section.
    
        linesmen = linesmen_table.text.strip().split('\n')
        linesmen = [linesman for linesman in linesmen if len(linesman) != 0]
        linesman_1 = linesmen[0]
        
        if len(linesmen) == 2:
            linesman_2 = linesmen[1]
        else:
            linesman_2 = '' # Check for this in next stage (compile_referees.py), might be present in standby section.

        referee_rows.append([game_id, referee_1, referee_2, linesman_1, linesman_2])

df_referees = pd.DataFrame(referee_rows, columns=['game_id', 'referee_1', 'referee_2', 'linesman_1', 'linesman_2'])
df_referees.sort_values(by=['game_id'], inplace=True)
print(df_referees.head(20))

df_referees.to_csv('../../Data/Raw/referees_raw.csv', index=False)