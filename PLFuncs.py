import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

#TODO: Write proper input and ouput format
#TODO: Write comments

def make_team_data(df, team):
    """

    """
    home_goals = f'{team}_goals'

    df_home_matches = df[df['home_team'] == team]
    df_home_matches = df_home_matches.drop(columns=['home_team'])
    df_home_matches = df_home_matches.rename(columns={'away_team': 'team', 
                                                'home_goals': home_goals, 
                                                'away_goals': 'opp_goals'})
    df_home_matches['home?'] = 'yes'

    df_away_matches = df[df['away_team'] == team]
    df_away_matches = df_away_matches.drop(columns=['away_team'])
    df_away_matches = df_away_matches.rename(columns={'home_team': 'team', 
                                                'away_goals': home_goals, 
                                                'home_goals': 'opp_goals'})
    df_away_matches = df_away_matches[['team',
                                home_goals,
                                'opp_goals',
                                'result',
                                'season']]
    df_away_matches['home?'] = 'no'



    df_team = pd.concat([df_home_matches, df_away_matches])
    df_team['goal_diff'] = df_team[home_goals] - df_team['opp_goals'] 

    return df_team.sort_index()

#TODO: Write proper input and output format
def make_team_vs_team_data():
    """

    """
    pass


