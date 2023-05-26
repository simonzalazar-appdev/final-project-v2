import datetime as datetime
import numpy as np
import pandas as pd
from datetime import datetime
from mplsoccer.pitch import VerticalPitch
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, ConnectionPatch, Arc
from matplotlib.font_manager import FontProperties
import data_structure as ds
import pickle


# filepath = "fifa_database/male_players (legacy).csv"
class FifaExtractor:
    def __init__(self, filepath=str, debug=True):
        self.df = pd.read_csv(filepath, low_memory=False)
        if debug == True:
            # just for debug: limiting to last two yrs. | -> or
            self.df = self.df[(self.df['fifa_version'] == 23) | (self.df['fifa_version'] == 25)]
            self.df = self.df[(self.df['league_id'] == 13) | (self.df['league_id'] == 14)]
        self.df['club_name'] = self.df['club_name'].str.replace(pat='Paris Saint Germain', repl='Paris Saint-Germain',
                                                                regex=False)
        self.df['club_name'] = self.df['club_name'].str.replace(pat='Real Madrid CF', repl='Real Madrid', regex=False)
        # adding the 'best_position' and 'value_million_eur' fields to each df
        self.df['best_position'] = self.df['player_positions'].str.split(',').str[0]
        self.df['2nd_position'] = self.df['player_positions'].str.split(',').str[1]
        # about 1k players through all FIFA versions have no values associated - the NaN 'value_eur' values are replaced with 0
        self.df['value_eur'] = self.df['value_eur'].fillna(0)
        self.df['value_million_eur'] = pd.to_numeric(self.df['value_eur'], errors='coerce') / 1000000
        self.players = pd.DataFrame()
        self.clubs = pd.DataFrame()
        self.player_stats = pd.DataFrame()
        self.team_stats = pd.DataFrame()
        self.formations_db = {}
        self.formations_dict = {
            '4-3-1-2': ['GK', 'RB|RWB', 'LCB|CB', 'RCB|CB', 'LB|LWB', 'CDM|CM', 'CDM|CM', 'CDM|CM', 'CAM|CF', 'CF|ST',
                        'CF|ST'],
            '4-3-2-1': ['GK', 'RB|RWB', 'LCB|CB', 'RCB|CB', 'LB|LWB', 'CDM|CM', 'CDM|CM', 'CDM|CM', 'CAM|CF', 'CAM|CF',
                        'CF|ST'],
            '4-3-3': ['GK', 'RB|RWB', 'LCB|CB', 'RCB|CB', 'LB|LWB', 'CDM|CM', 'CDM|CM', 'CDM|CM', 'RW|RF|ST', 'CF|ST',
                      'LW|LF|ST'],
            '4-4-2': ['GK', 'RB|RWB', 'RCB|CB', 'LCB|CB', 'LB|LWB', 'RM|RW', 'CDM|CM', 'CDM|CM', 'LM|LW', 'CF|ST',
                      'CF|ST'],
            '4-5-1': ['GK', 'RB|RWB', 'RCB|CB', 'LCB|CB', 'LB|LWB', 'RM|RW', 'CDM|CM', 'CDM|CM', 'LM|LW', 'CF|ST',
                      'CF|ST'],
            '3-4-1-2': ['GK', 'RCB|CB', 'CB', 'LCB|CB', 'RM|RW', 'CDM|CM', 'CDM|CM', 'LM|LW', 'CAM|CF', 'CF|ST',
                        'CF|ST'],
            '3-4-3': ['GK', 'RCB|CB', 'CB', 'LCB|CB', 'RWB|RM', 'CDM|CM', 'CDM|CM', 'LWB|LM', 'RW|RF|ST', 'CF|ST',
                      'LW|LF|ST'],
            '3-5-2': ['GK', 'RCB|CB', 'CB', 'LCB|CB', 'RM|RWB|RB', 'CDM|CM', 'CDM|CM', 'CDM|CM', 'LM|LWB|LB', 'CF|ST',
                      'CF|ST']}
        # dictionary used to calculate the player coordinates on the pitch, based on the number of players per team section such as defence, etc.
        plt.rcParams['axes.facecolor'] = 'white'
        plt.rcParams['figure.facecolor'] = 'white'
        self.xaxis_locations = {1: [40], 2: [30, 50], 3: [25, 40, 55], 4: [10, 30, 50, 70], 5: [10, 25, 40, 55, 70]}

    def build_player_df(self, dump=True, to_csv=False):
        # Players Database
        temp = pd.DataFrame(data=self.df[['player_id', 'short_name', 'long_name', 'dob', 'nationality_name']])
        temp = temp.drop_duplicates(subset=['player_id'])
        self.players = temp.rename(index=temp['player_id']).drop(columns=['player_id'])
        if dump:
            with open('players.pkl', 'wb') as fp:
                pickle.dump(self.players, fp)
                print('dataframe saved successfully to file')
        if to_csv == True:
            self.players.to_csv('players.csv')

    def read_player_df(self, filepath='players.pkl'):
        # read dictionary file (BYTE STREAM)
        with open(filepath, 'rb') as fp:
            self.players = pickle.load(fp)

    def build_clubs_df(self, dump=True, to_csv=False):
        # Teams Database
        temp = pd.DataFrame(data=self.df[['club_name', 'club_team_id', 'league_name', 'league_id']])
        temp = temp.drop_duplicates(subset=['club_team_id'])
        # reemplazar empty with nan
        temp['club_team_id'].replace('', np.nan, inplace=True)
        # droppear los nan
        temp.dropna(subset=['club_team_id'], inplace=True)
        self.clubs = temp.rename(index=temp['club_team_id']).drop(columns=['club_team_id'])
        if dump:
            with open('clubs.pkl', 'wb') as fp:
                pickle.dump(self.clubs, fp)
                print('dataframe saved successfully to file')
        if to_csv == True:
            self.clubs.to_csv('clubs.csv')

    def read_clubs_df(self, filepath='clubs.pkl'):
        # read dictionary file (BYTE STREAM)
        with open(filepath, 'rb') as fp:
            self.clubs = pickle.load(fp)

    def build_player_stats_df(self, dump=True, to_csv=False):
        # Players Stats
        drop_cols = ['short_name', 'long_name', 'fifa_version', 'fifa_update', 'dob', 'league_name', 'club_name',
                     'club_joined_date', 'club_contract_valid_until_year', 'nationality_id', 'nationality_name',
                     'nation_team_id', 'nation_position', 'nation_jersey_number', 'real_face']
        player_stats = self.df.copy().drop(columns=drop_cols)
        player_dict = self.players.to_dict(orient='index')
        player_dict_date = {}

        for i, col in enumerate(['perf_date', 'season', 'latest']):
            player_stats.insert(i + 1, col, value=np.nan)

        for index, row in player_stats.iterrows():
            player_stats.at[index, 'perf_date'] = datetime.strptime(row['fifa_update_date'], '%Y-%m-%d')
            player_stats.at[index, 'season'] = player_stats.at[index, 'perf_date'].year
            # to later fill the latest part
            if player_stats.at[index, 'player_id'] not in player_dict_date:
                player_dict_date[player_stats.at[index, 'player_id']] = [player_stats.at[index, 'perf_date'], index]
            elif player_dict_date[player_stats.at[index, 'player_id']][0] < player_stats.at[index, 'perf_date']:
                player_dict_date[player_stats.at[index, 'player_id']] = [player_stats.at[index, 'perf_date'], index]
            player_stats.at[index, 'latest'] = False
            # print(f"done {player_stats.at[index, 'player_id']}")

        for player_id, value in player_dict_date.items():
            # player_stats.loc[player_stats.index == value[0], 'latest'] = True
            player_stats.at[value[1], 'latest'] = True
            # player_stats.loc[player_stats['player_id'] == 1]

        self.player_stats = player_stats.drop(columns=['fifa_update_date'])
        if dump:
            with open('player_stats.pkl', 'wb') as fp:
                pickle.dump(self.player_stats, fp)
                print('dataframe saved successfully to file')
        if to_csv == True:
            self.player_stats.to_csv('player_stats.csv')

    def read_player_stats_df(self, filepath='player_stats.pkl'):
        # read dictionary file (BYTE STREAM)
        with open(filepath, 'rb') as fp:
            self.player_stats = pickle.load(fp)

    def get_best_formation(self, club_id=0, season=int, measurement='overall'):
        formation_df = self.player_stats
        if club_id != 0:
            formation_df = formation_df[formation_df['club_team_id'] == club_id]
        optimal_formation = {}
        for formation in self.formations_dict:
            optimal_formation[formation] = {}
            copied_df = formation_df[formation_df['season'] == season].copy()
            pos_list = self.formations_dict[formation]
            pos_list_2nd = []
            no_players = 0

            for pos in pos_list:
                # get best record based on 'overall' or 'potential', then drop that record from copied df, so that it cannot be selected again
                if not np.isnan(copied_df[copied_df['best_position'].str.contains(pos)][measurement].max()):
                    # when checking e.g. 'RB|RWB', the '|' means or.
                    # idxmax retorna el index del maximum value
                    # loc cuando es con [[]] trae dataframe, cuando es [] trae valor
                    idx_best_plyr = copied_df[copied_df['best_position'].str.contains(pos)][measurement].idxmax()
                    if not pos in optimal_formation[formation]:  # si no existe la lista
                        optimal_formation[formation][pos] = []
                    optimal_formation[formation][pos].append({'player_id': copied_df.loc[idx_best_plyr]['player_id'],
                                                              measurement: copied_df.loc[idx_best_plyr][measurement]})
                    copied_df.drop(copied_df[copied_df['best_position'].str.contains(pos)][measurement].idxmax(),
                                   inplace=True)
                    no_players += 1
                    # print(f'copied {pos}')
                else:
                    pos_list_2nd.append(pos)

            copied_df = copied_df[~copied_df['2nd_position'].isnull()]
            for pos in pos_list_2nd:
                # get best record based on 'overall' or 'potential', then drop that record from copied df, so that it cannot be selected again
                if not np.isnan(copied_df[copied_df['2nd_position'].str.contains(pos)][measurement].max()):
                    # when checking e.g. 'RB|RWB', the '|' means or.
                    # idxmax retorna el index del maximum value
                    # loc cuando es con [[]] trae dataframe, cuando es [] trae valor
                    idx_best_plyr = copied_df[copied_df['2nd_position'].str.contains(pos)][measurement].idxmax()
                    if not pos in optimal_formation[formation]:  # si no existe la lista
                        optimal_formation[formation][pos] = []
                    optimal_formation[formation][pos].append({'player_id': copied_df.loc[idx_best_plyr]['player_id'],
                                                              measurement: copied_df.loc[idx_best_plyr][measurement]})
                    copied_df.drop(copied_df[copied_df['2nd_position'].str.contains(pos)][measurement].idxmax(),
                                   inplace=True)
                    no_players += 1
                    # print(f'copied {pos}')
            # print(f'current lineup: {optimal_formation[formation]}, len: {len(optimal_formation[formation])}')
            if no_players == 11:
                optimal_formation[formation]['total_score'] = sum([item[measurement] for p in pos_list for item in
                                                                   optimal_formation[formation][
                                                                       p]])  # use list comprehension
                optimal_formation[formation]['is_best'] = False
            else:  # some formations might not find 11 available players - these ones need to be excluded from any possible calcuation
                optimal_formation.pop(formation)
                # print('deleted')

        # aca me devuelve la key que es la formacion, y utiliza como key para max los puntajes.
        # formation_score = {key: val['total_score'] for key, val in optimal_formation.items()} #dictionary comprehension
        # best_formation = max(formation_score)
        best_formation = max(optimal_formation, key=lambda x: optimal_formation[x]['total_score'])
        optimal_formation[best_formation]['is_best'] = True
        return {
            'season': season,
            'best_formation': best_formation,
            'measurement': measurement,
            'opt_formations_dict': optimal_formation
        }

    # Build best formations historical for all clubs
    def build_formations_all(self, measurement='overall', to_csv=True, dump=True):
        for season_i in self.player_stats['season'].unique():
            unique_teams = self.player_stats[self.player_stats['season'] == season_i]['club_team_id'].unique()
            unique_teams = unique_teams[~np.isnan(unique_teams)]  # ~ is the not operator. To drop nan vals.
            self.formations_db[season_i] = {}
            for team_id_i in unique_teams:
                try:
                    temp = self.get_best_formation(club_id=team_id_i, season=season_i, measurement=measurement)
                    temp.pop('season')
                    self.formations_db[season_i][team_id_i] = temp
                except ValueError:
                    print(f"Didn't include {self.clubs.loc[team_id_i]['club_name']}")
        if to_csv:
            temp_df = pd.DataFrame.from_dict(self.formations_db)
            temp_df.to_csv('formations_db.csv')
        if dump:
            # save dictionary to person_data.pkl file (BYTE STREAM)
            with open('formations_db.pkl', 'wb') as fp:
                pickle.dump(self.formations_db, fp)
                print('dictionary saved successfully to file')

    def read_formations_db(self, filepath='formations_db.pkl'):
        # read dictionary file (BYTE STREAM)
        with open(filepath, 'rb') as fp:
            self.formations_db = pickle.load(fp)

    def read_formations_db_old(self, filepath='formations_db.csv'):
        temp_dict = pd.read_csv(filepath, index_col='Unnamed: 0', low_memory=False).to_dict()
        # changing keys of dictionary to float
        self.formations_db = {float(key): value for key, value in temp_dict.items()}

    # Team Stats
    def build_team_stats(self, dump=True, to_csv=True):
        columns_array = [*ds.player_stats_vars]
        columns_array += [f'var_player_{i + 1}_' + var for i in range(11) for var in ds.player_vars]  # for 11 p
        team_stats = pd.DataFrame(columns=columns_array)
        for season_i, season_value in self.formations_db.items():
            #print(f'season *** {season_i}, season value*** {season_value}')
            #print(f'season *** {season_i}')
            for team_i, team_value in season_value.items():
                #print(f'team ****{team_i}, teamvalue**** {team_value}')
                #print(f'team ****{team_i}')
                initial_stats = {'team_id': team_i, 'season': season_i, 'formation': team_value['best_formation'],
                                 'coach_id': 'to_be_implemented'}
                player_stats_row = {}
                player_i = 0
                # cant use enumerate bc pos might have more than one player
                for player_pos, pos_players in team_value['opt_formations_dict'][team_value['best_formation']].items():
                    #print(player_pos)
                    #print(player_i)
                    if player_i > 10: break
                    for pos_values in pos_players:
                        player_i += 1
                        player_id = pos_values['player_id']
                        #print(player_id)
                        ante_var = f'var_player_{player_i}_'
                        player_stats_row.update({ante_var + 'actual_position': player_pos, ante_var + 'id': player_id})
                        last_data = self.player_stats[(self.player_stats['player_id'] == player_id) & (
                                self.player_stats['season'] == season_i)].iloc[-1]
                        if type(last_data['player_tags']) == str:
                            tags = last_data['player_tags'].replace(' ', '').split(',')
                        else:
                            tags = []
                        if type(last_data['player_traits']) == str:
                            traits = last_data['player_traits'].replace(' ', '').split(',')
                        else:
                            traits = []
                        for var in ds.player_vars[2:]:  # para skippear id y actual_position
                            if var[:5] == 'tag_#':
                                player_stats_row[ante_var + var] = (var in tags)
                            elif var[:5] == 'trait':
                                player_stats_row[ante_var + var] = (var in traits)
                            else:
                                player_stats_row[ante_var + var] = last_data[var]
                        #print(f'finished player {pos_values}')
                        #print(f'full_row so far{player_stats_row}')

                full_row = {**initial_stats, **player_stats_row}
                team_stats.loc[len(team_stats)] = full_row
                #print(f'appended {full_row}')
        self.team_stats = team_stats
        if dump:
            with open('team_stats.pkl', 'wb') as fp:
                pickle.dump(self.team_stats, fp)
                print('dataframe saved successfully to file')
        if to_csv:
            self.team_stats.to_csv('team_stats.csv')

    def read_team_stats(self, filepath='team_stats.pkl'):
        # read dictionary file (BYTE STREAM)
        with open(filepath, 'rb') as fp:
            self.team_stats = pickle.load(fp)

    def build_results_df(self, filepath='results_database/eplmatchesv4 debug.csv', dump=True, to_csv=False):
        # Players Database
        self.results_db = pd.read_csv(filepath, low_memory=False)
        if dump:
            with open('results.pkl', 'wb') as fp:
                pickle.dump(self.results_db, fp)
                print('dataframe saved successfully to file')
        if to_csv:
            self.results_db.to_csv('results.csv')
#fifa_1.results_db= pd.read_csv('results_database/eplmatchesv4.csv', low_memory=False)
    def read_results_db(self, filepath='results.pkl'):
        # read dictionary file (BYTE STREAM)
        with open(filepath, 'rb') as fp:
            self.results_db = pickle.load(fp)

    def build_sample_df(self, dump=True, to_csv=True):
        print(f'team 1 is always home')
        columns_array = ['season', 'team_1_id', 'team_2_id', 'team_1_score',
                         'team_2_score', 'team_1_formation', 'team_2_formation']
        columns_array += [f'team_1_var_player_{i + 1}_' + var for i in range(11) for var in ds.player_vars]  # for 11 p
        columns_array += [f'team_2_var_player_{i + 1}_' + var for i in range(11) for var in ds.player_vars]  # for 11 p
        sample_df = pd.DataFrame(columns=columns_array)
        for index, result in self.results_db.iterrows():
            team_1_id = result['home_team_id']
            team_2_id = result['away_team_id']
            team_1_score = result['home_team_score']
            team_2_score = result['away_team_score']
            season = result['season']
            full_row= {'season': season,'team_1_id': team_1_id, 'team_2_id':team_2_id,'team_1_score':team_1_score,
                       'team_2_score':team_2_score,'team_1_formation':'', 'team_2_formation':''}
            team_list = [team_1_id,team_2_id]
            for team_i in range(1,3):
                ante_var = f'team_{team_i}_'
                team_row = self.team_stats[(self.team_stats['team_id'] == team_list[team_i - 1]) & (self.team_stats['season'] == season)].iloc[-1]
                full_row[f'team_{team_i}_formation'] = team_row['formation']
                for var in [f'var_player_{i + 1}_' + var for i in range(10) for var in ds.player_vars]:
                    full_row[ante_var + var] = team_row[var]
            sample_df.loc[len(sample_df)] = full_row
            self.sample_df = sample_df

        if dump:
            with open('sample_df.pkl', 'wb') as fp:
                pickle.dump(self.sample_df, fp)
                print('dataframe saved successfully to file')
        if to_csv:
            self.sample_df.to_csv('sample_df.csv')

    def read_sample_df(self, filepath='sample_df.pkl'):
        # read dictionary file (BYTE STREAM)
        with open(filepath, 'rb') as fp:
            self.sample_df = pickle.load(fp)

    # meter un help method
    def build_all_df(self, build_formations=False, to_csv=True):
        self.build_player_df(to_csv=to_csv)
        self.build_clubs_df(to_csv=to_csv)
        self.build_player_stats_df(to_csv=to_csv)
        if build_formations: self.build_formations_all()
        self.build_team_stats(to_csv=to_csv)
        self.build_results_df()
        self.build_sample_df()

    def read_all_df(self):
        self.read_player_df()
        self.read_clubs_df()
        self.read_player_stats_df()
        self.read_formations_db()
        self.read_team_stats()
        self.read_results_db()
        self.read_sample_df

    # Lineup creation
    # functions for the lineup visualizations
    # original code taken from https://towardsdatascience.com/advanced-sports-visualization-with-pandas-matplotlib-and-seaborn-9c16df80a81b

    # initialize_df(file, players, clubs, player_stats)

    # z_1 = get_best_formation(club_id=241, season=2022)
    # conversion for draw
    def conv_draw(self, formation_combination=dict, formation=''):
        df = self.player_stats
        if formation == '':
            formation_rt = formation_combination['best_formation']
        df = df[df['season'] == formation_combination['season']]
        player_list = {}
        for pos, players_i in formation_combination['opt_formations_dict'][formation_rt].items():
            if pos == 'total_score': break  # break after looping through players
            for player in players_i:
                # player_in_df = df.loc[(df['player_id'] == player['player_id']) & (df['season'] == player['player_id'])]
                player_in_df = df.loc[df['player_id'] == player['player_id']].iloc[-1]  # iloc -1 to get the latest one
                player_id = player['player_id']
                short_name = self.players.loc[player_id]['short_name']
                player_list[short_name] = []
                player_list[short_name].append(player_in_df['best_position'])
                player_list[short_name].append(player_in_df[formation_combination['measurement']])
                player_list[short_name].append(player_in_df['age'])
                player_list[short_name].append(player_in_df['value_million_eur'])
                player_list[short_name].append(self.clubs.loc[player_in_df['club_team_id']]['club_name'])
        return formation_rt, player_list

    # x_2, y_2 = conv_draw(formation_combination=z_1)
    def get_players_section_coord_col(self, players_coord_dict, players_col_dict, color_val, players_in_section,
                                      yaxis_val,
                                      team_order):
        if team_order == 'home':
            xaxis_val = self.xaxis_locations
        elif team_order == 'away':
            xaxis_val = {k: v[::-1] for k, v in
                         self.xaxis_locations.items()}  # reversing the X-axis for the opponent lineup
            yaxis_val = 120 - yaxis_val  # total pitch length is 120, so positions have the same distintance from the own team's goal
        else:
            raise ValueError('Invalid team_order value provided - Can be only "home" or "away"')
        for idx, val in enumerate(range(players_in_section)):
            players_coord_dict[len(players_coord_dict)] = [xaxis_val[players_in_section][idx], yaxis_val]
            players_col_dict[len(players_col_dict)] = color_val
        return players_coord_dict, players_col_dict

    def get_player_locations_colors(self, formation, team_type='home'):
        lineup_sections = formation.split('-')
        defenders = int(lineup_sections[0])
        midfielders = int(lineup_sections[1])
        if len(lineup_sections) == 4:
            # trequartista spots are occupied
            trequartistas = int(lineup_sections[2])
            strikers = int(lineup_sections[3])
        elif len(lineup_sections) == 3:
            trequartistas = 0
            strikers = int(lineup_sections[2])
        if len(lineup_sections) not in [3, 4] or (defenders + midfielders + trequartistas + strikers) != 10:
            raise ValueError(
                'Formation invalid - Missing or extra player sections other than defence, midfield, and offence')
        # getting the player locations and colors in two dictionaries that are gradually populated
        locations_dict = {}
        colors_dict = {}
        locations_dict, colors_dict = self.get_players_section_coord_col(locations_dict, colors_dict, 'darkslategrey',
                                                                         1,
                                                                         112,
                                                                         team_type)  # GK
        locations_dict, colors_dict = self.get_players_section_coord_col(locations_dict, colors_dict, 'blue', defenders,
                                                                         98,
                                                                         team_type)  # DEFs
        locations_dict, colors_dict = self.get_players_section_coord_col(locations_dict, colors_dict, 'gold',
                                                                         midfielders,
                                                                         84,
                                                                         team_type)  # MIDs
        if trequartistas > 0:
            locations_dict, colors_dict = self.get_players_section_coord_col(locations_dict, colors_dict, 'red',
                                                                             trequartistas,
                                                                             77, team_type)  # CAMs
        locations_dict, colors_dict = self.get_players_section_coord_col(locations_dict, colors_dict, 'red', strikers,
                                                                         70,
                                                                         team_type)  # STRs
        return locations_dict, colors_dict

    def draw_pitch(self, axis):
        # pitch outline and centre line
        pitch = Rectangle([0, 0], width=80, height=120, edgecolor='black', fill=False)  # facecolor='#23E04F'
        # left and right penalty area and midline
        left_penalty = Rectangle([22.3, 0], width=35.3, height=14.6, fill=False)
        right_penalty = Rectangle([22.3, 105.4], width=35.3, height=14.6, fill=False)
        midline = ConnectionPatch([0, 60], [80, 60], 'data', 'data')
        # left and right six-yard box
        left_six_yard = Rectangle([32, 0], width=16, height=4.9, fill=False)
        right_six_yard = Rectangle([32, 115.1], width=16, height=4.9, fill=False)
        # prepare circles
        centre_circle = plt.Circle((40, 60), 8.1, color='black', fill=False)
        centre_spot = plt.Circle((40, 60), 0.4, color='black')
        # penalty spots and arcs around penalty boxes
        # left_pen_spot = plt.Circle((40, 9.7), 0.4, color='black')
        # right_pen_spot = plt.Circle((40, 110.3), 0.4, color='black')
        left_arch = Arc((40, 9.5), width=16.2, height=16.2, angle=90, theta1=310, theta2=50, color='black')
        right_arch = Arc((40, 110.4), width=16.2, height=16.2, angle=90, theta1=130, theta2=230, color='black')
        elements_list = [pitch, left_penalty, right_penalty, midline, left_six_yard, right_six_yard, centre_circle,
                         centre_spot,
                         left_arch, right_arch]
        for element in elements_list:
            axis.add_patch(element)

    def draw_teams_matchup(self, season=int, home_team_name='', away_team_name='',
                           home_team_formation='', away_team_formation='', measurement='overall', drawn_pitch='manual'):
        df = self.player_stats
        # get the club id
        home_team_id = self.clubs.loc[self.clubs['club_name'] == home_team_name].index[0]
        away_team_id = self.clubs.loc[self.clubs['club_name'] == away_team_name].index[0]
        # setting the figure where the matchup will be plotted
        fig = plt.figure()
        fig.set_size_inches(10, 14)
        ax = fig.add_subplot(1, 1, 1)
        if drawn_pitch == 'mplsoccer':  # plotting the fancy pitch from 'mplsoccer'
            pitch = VerticalPitch(pitch_color='grass', line_color='white', stripe=True)
            pitch.draw(ax=ax)
        else:  # calling the function that draws the pitch
            self.draw_pitch(ax)
        # setting the field columns shown on the right-hand side of the figure
        if measurement == 'overall':
            note_columns = ('Position', 'Player Name', 'Overall Attribute', 'Age', 'Player Value (in €M)', 'Club Name')
        elif measurement == 'potential':
            note_columns = (
                'Position', 'Player Name', 'Potential Attribute', 'Age', 'Player Value (in €M)', 'Club Name')
        else:
            raise ValueError('Measurement value provided is not valid (nor "overall" neither "potential")')
        # drawing home team lineup
        home_formation, home_players = self.conv_draw(formation_combination=self.get_best_formation(
            club_id=home_team_id,
            season=season,
            measurement=measurement))
        home_players_list = list(home_players)
        home_locations_dict, home_colors_dict = self.get_player_locations_colors(home_formation, team_type='home')
        for i in range(len(home_players_list)):
            player_x, player_y = home_locations_dict[i][0], home_locations_dict[i][1]
            player_color = home_colors_dict[i]
            if '. ' in home_players_list[i]:
                player_name = home_players_list[i].split('. ', 1)[1]
            else:
                player_name = home_players_list[i]
            plt.annotate(player_name,
                         xy=(player_x, player_y), xytext=(0, 18),
                         bbox=dict(boxstyle='round', fc='w'), va='center', ha='center', textcoords='offset points')
            plt.scatter(player_x, player_y, s=250, c=player_color)
        # adding notes on the right-hand side of the home team
        home_team_list = []
        for k, v in home_players.items():
            home_team_list.append([v[0], k, v[1], v[2], v[3], v[4]])
        home_sum_rating = home_sum_age = home_sum_value = 0
        for k, v in home_players.items():
            home_sum_rating = home_sum_rating + v[1]
            home_sum_age = home_sum_age + v[2]
            home_sum_value = home_sum_value + v[3]
        home_notes = [[home_team_name],
                      ['Average rating: {avg_rating}'.format(avg_rating=round((home_sum_rating / 11), 1))],
                      ['Average age: {avg_age}'.format(avg_age=round((home_sum_age / 11), 1))],
                      ['Total Value (in €M): {total_value:,}'.format(total_value=round(home_sum_value, 1))]]
        plt_table = plt.table(cellText=home_team_list, colLabels=note_columns,
                              colWidths=[0.3, 0.5, 0.35, 0.2, 0.4, 0.5], cellLoc='right', loc='right',
                              bbox=[1, 0.505, 1.7, 0.36])
        plt_table.scale(1.5, 2)
        for (row, col), cell in plt_table.get_celld().items():
            if (row == 0):
                cell.set_text_props(fontproperties=FontProperties(weight='bold'))
        plt_home_notes = plt.table(cellText=home_notes, cellLoc='left', loc='left', bbox=[0.9, 0.87, 1.1, 0.12])
        for key, cell in plt_home_notes.get_celld().items():
            cell.set_linewidth(0)
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))
        # drawing away team lineup
        away_formation, away_players = self.conv_draw(formation_combination=self.get_best_formation(
            club_id=away_team_id,
            season=season,
            measurement=measurement))
        away_players_list = list(away_players)
        away_locations_dict, away_colors_dict = self.get_player_locations_colors(away_formation, team_type='away')
        for i in range(len(away_players_list)):
            player_x, player_y = away_locations_dict[i][0], away_locations_dict[i][1]
            player_color = away_colors_dict[i]
            if '. ' in away_players_list[i]:
                player_name = away_players_list[i].split('. ', 1)[1]
            else:
                player_name = away_players_list[i]
            plt.annotate(player_name,
                         xy=(player_x, player_y), xytext=(0, 18),
                         bbox=dict(boxstyle='round', fc='w'), va='center', ha='center', textcoords='offset points')
            plt.scatter(player_x, player_y, s=250, c=player_color)
        # adding notes on the right-hand side of the away team
        away_team_list = []
        for k, v in away_players.items():
            away_team_list.append([v[0], k, v[1], v[2], v[3], v[4]])
        away_sum_rating = away_sum_age = away_sum_value = 0
        for k, v in away_players.items():
            away_sum_rating = away_sum_rating + v[1]
            away_sum_age = away_sum_age + v[2]
            away_sum_value = away_sum_value + v[3]
        away_notes = [[away_team_name],
                      ['Average rating: {avg_rating}'.format(avg_rating=round((away_sum_rating / 11), 1))],
                      ['Average age: {avg_age}'.format(avg_age=round((away_sum_age / 11), 1))],
                      ['Total Value (in €M): {total_value:,}'.format(total_value=round(away_sum_value, 1))]]
        plt_table = plt.table(cellText=away_team_list, colLabels=note_columns,
                              colWidths=[0.3, 0.5, 0.35, 0.2, 0.4, 0.5], cellLoc='right', loc='right',
                              bbox=[1, 0.015, 1.7, 0.36])
        plt_table.scale(1.5, 2)
        for (row, col), cell in plt_table.get_celld().items():
            if (row == 0):
                cell.set_text_props(fontproperties=FontProperties(weight='bold'))
        plt_away_notes = plt.table(cellText=away_notes, cellLoc='left', loc='left', bbox=[0.9, 0.38, 1.1, 0.12])
        for key, cell in plt_away_notes.get_celld().items():
            cell.set_linewidth(0)
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))
        # adding the final settings to the plot
        plt.xlim(-2, 82)
        plt.ylim(-2, 122)
        plt.axis('off')
        plt.show()


#fifa_1 = FifaExtractor(filepath)
#fifa_1.read_all_df()
#fifa_1.build_sample_df()
# fifa_1.build_all_df()
# fifa_1.read_formations_db()
#fifa_1.build_team_stats()
# fifa_1.draw_teams_matchup(home_team_name='Manchester City', away_team_name='Manchester United', season=2022, drawn_pitch='mplsoccer')
