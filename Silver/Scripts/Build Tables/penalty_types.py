import sys
from pathlib import Path
import json
import pandas as pd

penalty_severities_path = '../../Data/Tables/penalty_severities.csv'
p = Path(penalty_severities_path)
if not p.exists():
    print('Penalty severities must be extracted first via the Silver/Scripts/Build Tables/penalty_severities.py script.')
    sys.exit(1)

df_penalty_severities = pd.read_csv(penalty_severities_path)

p = Path('../../../Bronze/Data/Landings')
if not p.exists():
    print('Landings must be downloaded first via the Bronze/Scripts/NHL API Calls/get_landings.py script.')
    sys.exit(1)

penalty_type_rows = []

for landing_path in p.rglob('*.json'):
    with open(landing_path, 'r') as f:
        data = json.load(f)
        for period in range(3):
            period_penalties = data['summary']['penalties'][period]['penalties']
            for penalty in period_penalties:
                penalty_type = penalty['descKey']
                penalty_severity = penalty['type']
                penalty_minutes = penalty['duration']
                
                if penalty_severity == 'MIN' and penalty_minutes == 4:
                    penalty_severity = 'DMIN' # double minor
                if penalty_severity == 'BEN' and penalty_minutes == 4:
                    penalty_severity = 'DBEN' # double bench minor
                if penalty_severity == 'GAM' and penalty_minutes == 0:
                    penalty_severity = 'CGAM' # coach game misconduct
                
                penalty_severity_id = df_penalty_severities[df_penalty_severities['abbreviation']==penalty_severity].iloc[0,0]
                penalty_type_rows.append([penalty_type, penalty_severity_id])

df_penalty_types = pd.DataFrame(penalty_type_rows, columns=['name', 'penalty_severity_id'])
df_penalty_types = df_penalty_types.drop_duplicates(subset=['name', 'penalty_severity_id'], keep='first')
df_penalty_types = df_penalty_types.reset_index(drop=True).reset_index()
df_penalty_types.rename(columns={'index': 'id'}, inplace=True)
df_penalty_types = df_penalty_types[['id', 'penalty_severity_id', 'name']]

# print(df_penalty_types.head(20))

df_penalty_types.to_csv('../../Data/Tables/penalty_types.csv', index=False)