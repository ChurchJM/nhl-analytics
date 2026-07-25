import sys
from pathlib import Path
import json
import pandas as pd

p = Path('../../../Bronze/Data/Landings')
if not p.exists():
    print('Landings must be downloaded first via the Bronze/Scripts/NHL API Calls/get_landings.py script.')
    sys.exit(1)

penalty_severity_rows = []

for landing_path in p.rglob('*.json'):
    with open(landing_path, 'r') as f:
        data = json.load(f)
        for period in range(3):
            period_penalties = data['summary']['penalties'][period]['penalties']
            for penalty in period_penalties:
                penalty_severity = penalty['type']
                penalty_minutes = penalty['duration'] # STATISTICAL minutes, not power play time (corrected later).
                
                if penalty_severity == 'MIN' and penalty_minutes == 4:
                    penalty_severity = 'DMIN' # double minor
                if penalty_severity == 'BEN' and penalty_minutes == 4:
                    penalty_severity = 'DBEN' # double bench minor
                if penalty_severity == 'MAT':
                    penalty_minutes = 15 # Should be 10 minutes for the ejection and 5 minutes for the on-ice power play in all cases I think
                if penalty_severity == 'GAM' and penalty_minutes == 0:
                    penalty_severity = 'CGAM' # coach game misconduct

                penalty_severity_rows.append([penalty_severity, penalty_minutes])

df_penalty_severities = pd.DataFrame(penalty_severity_rows, columns=['abbreviation', 'stat_minutes'])

penalty_severity_names = {
    'MIN' : 'minor',
    'MAJ' : 'major',
    'BEN' : 'bench minor',
    'MIS' : 'misconduct',
    'DMIN' : 'double minor',
    'PS' : 'penalty shot',
    'GAM' : 'game misconduct',
    'MAT' : 'match penalty',
    'CGAM' : 'coach game misconduct',
    'DBEN' : 'double bench minor'
}

# The statistical minutes (e.g., the toal PIM listed on box scores) are different than the actual on-ice power player time for these penalties.
power_play_minutes = {
    'MAT' : 5,
    'MIS' : 0,
    'GAM' : 0
}

df_penalty_severities['name'] = df_penalty_severities.apply(lambda row: penalty_severity_names[row['abbreviation']], axis=1)
df_penalty_severities['pp_minutes'] = df_penalty_severities.apply(
    lambda row: row['stat_minutes'] if row['abbreviation'] not in power_play_minutes else power_play_minutes[row['abbreviation']], axis=1)
df_penalty_severities = df_penalty_severities[['name', 'abbreviation', 'pp_minutes', 'stat_minutes']]
df_penalty_severities = df_penalty_severities.drop_duplicates(subset=['name', 'abbreviation'], keep='first').sort_values(by='stat_minutes')
df_penalty_severities = df_penalty_severities.reset_index(drop=True).reset_index()
df_penalty_severities['index'] = df_penalty_severities['index']+1
df_penalty_severities.rename(columns={'index': 'id'}, inplace=True)

# print(df_penalty_severities.head(20))

df_penalty_severities.to_csv('../../Data/Tables/penalty_severities.csv', index=False)