import pandas as pd

# There are only 32 teams, so I built this table manually, using NHL team IDs.
# Thought about including arena name, but this would be a slowly changing dimension so skipped it for now.
team_rows = [
    [1, 'New Jersey Devils', 'NJD'],
    [2, 'New York Islanders', 'NYI'],
    [3, 'New York Rangers', 'NYR'],
    [4, 'Philadelphia Flyers', 'PHI'],
    [5, 'Pittsburgh Penguins', 'PIT'],
    [6, 'Boston Bruins', 'BOS'],
    [7, 'Buffalo Sabres', 'BUF'],
    [8, 'Montreal Canadiens', 'MTL'],
    [9, 'Ottawa Senators', 'OTT'],
    [10, 'Toronto Maple Leafs', 'TOR'],
    [12, 'Carolina Hurricanes', 'CAR'],
    [13, 'Florida Panthers', 'FLA'],
    [14, 'Tampa Bay Lightning', 'TBL'],
    [15, 'Washington Capitals', 'WSH'],
    [16, 'Chicago Blackhawks', 'CHI'],
    [17, 'Detroit Red Wings', 'DET'],
    [18, 'Nashville Predators', 'NSH'],
    [19, 'St. Louis Blues', 'STL'],
    [20, 'Calgary Flames', 'CGY'],
    [21, 'Colorado Avalanche', 'COL'],
    [22, 'Edmonton Oilers', 'EDM'],
    [23, 'Vancouver Canucks', 'VAN'],
    [24, 'Anaheim Ducks', 'ANA'],
    [25, 'Dallas Stars', 'DAL'],
    [26, 'Los Angeles Kings', 'LAK'],
    [28, 'San Jose Sharks', 'SJS'],
    [29, 'Columbus Blue Jackets', 'CBJ'],
    [30, 'Minnesota Wild', 'MIN'],
    [52, 'Winnipeg Jets', 'WPG'],
    [53, 'Arizona Coyotes', 'ARI'],
    [54, 'Vegas Golden Knights', 'VGK'],
    [55, 'Seattle Kraken', 'SEA'],
    [68, 'Utah Mammoth', 'UTA']
]

df_teams = pd.DataFrame(team_rows, columns=['id', 'full_name', 'abbreviation'])

# print(df_teams.head())

df_teams.to_csv('../../Data/Tables/teams.csv', index=False)