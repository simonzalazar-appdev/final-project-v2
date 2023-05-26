import data_structure as ds
import fifa_extractorV3 as fe
import pandas as pd

def return_vars():
    return ds.player_vars

def return_clubs():
    import csv
    with open('clubs.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(row[0].split(',')[1])

def build_database():
  global extractor
  extractor = fe.FifaExtractor('initial_db/male_players (legacy).csv')
  extractor.build_all_df(build_formations=True)
  #print('database built')

def read_database():
  global extractor
  extractor = fe.FifaExtractor('initial_db/male_players (legacy).csv')
  extractor.read_all_df()
  return extractor

def return_clubs2():
  extractor = read_database()
  clubs_list = extractor.clubs['club_name'].to_string(header=False, index=False).split('\n')
  clubs_list = [','.join(ele.split()) for ele in clubs_list]
  return clubs_list

def return_seasons():
  extractor = read_database()
  seasons = extractor.player_stats['season'].unique()
  return seasons

def build_season_list():
    extractor = read_database()
    seasons = pd.Dataframe(extractor.player_stats['season'].unique())
    seasons.to_csv('seasons.csv')
    print('built!')

def build_vars_list():
    pd.DataFrame(ds.player_vars[2:]).to_csv('vars.csv')
    print('built!')

def build_model_params():
    params_db = pd.read_csv('selected_params.csv')
    team_home = params_db['team_home'][0]
    team_away = params_db['team_away'][0]
    season = params_db['season'][0]
    vars_sel = []
    for var in ds.player_vars:
        if var in params_db.columns:
            vars_sel.append(var)
    return {'team_home':team_home,
            'team_away': team_away,
            'season': season,
            'variables': vars_sel}
