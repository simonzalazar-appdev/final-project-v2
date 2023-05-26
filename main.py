import numpy as np
import sklearn as skl
import statsmodels as stats
import statsmodels.api as sm
import python_ruby_bridge as prb
from sklearn.model_selection import train_test_split

def build_model_v1(team: str):
    extractor = prb.read_database()
    extractor.read_sample_df()
    parameters = prb.build_model_params()
    sample_df = extractor.sample_df
    sample_df = sample_df[sample_df['season'] == parameters['season']]
    sample_df, validation_df = train_test_split(sample_df, test_size=0.2)
    selected_vars = []
    for var in parameters['variables']:
        for player_i in range(1,11):
            selected_vars.append(f'team_1_var_player_{player_i}_{var}')
    #print(selected_vars)
    x = sample_df[selected_vars]
    y = sample_df[team]
    x = sm.add_constant(x)
    #model = sm.GLM(y, x)
    model = sm.OLS(y, x)
    results = model.fit()
    return {'model_obj':model, 'model':results, 'vars': selected_vars}

def build_match():
    team_home = build_model_v1(team='team_1_score')
    team_away = build_model_v1(team='team_2_score')
    #print(team_home['results'])
    return team_home, team_away
    #missing model iteration with AIC. missing prediction. missing logistic model with probs.

def predict_match():
    model1 = build_model_v1(team='team_1_score')
    model2 = build_model_v1(team='team_2_score')
    extractor = prb.read_database()
    extractor.read_sample_df()
    parameters = prb.build_model_params()
    sample_df = extractor.sample_df
    x_new = sample_df.loc[sample_df['season'] == parameters['season']]
    x_new = x_new.loc[x_new['team_1_id'] == parameters['team_home']]
    x_new = x_new[model1['vars']]
    x_new.insert(0, "constant", 0, True)
    team_1_score = model1['model'].predict(x_new).iloc[0]
    #print(team_1_score)
    x_new = sample_df.loc[sample_df['season'] == parameters['season']]
    x_new = x_new.loc[x_new['team_1_id'] == parameters['team_home']]
    x_new = x_new[model2['vars']]
    x_new.insert(0, "constant", 0, True)
    team_2_score = model2['model'].predict(x_new).iloc[0]
    #print(team_2_score)
    return [round(team_1_score), round(team_2_score)]


#build_match()
#team_home = build_model_v1(team='team_1_score')
#predict_match()
