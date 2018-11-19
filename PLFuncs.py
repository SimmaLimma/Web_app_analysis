# TODO: Rename file 

import pandas as pd 
import numpy as np 

# TODO: Make it a class
class PLData:

    def __init__(self):

        # All data from results.csv
        self.data = []

    def load_data(self):
        pass

    def make_team_data(self, df, team):
        """

        """

        # TODO: Refactor so that df-search is made as 
        #   "home_team or away_team" == team, in order to skip
        #   unnecessery sort_index and better DRY
        df_home_matches = df[df['home_team'] == team]
        df_home_matches = df_home_matches.drop(columns=['home_team'])
        df_home_matches = df_home_matches.rename(columns={'away_team': 'team', 
                                                    'home_goals': 'made_goals', 
                                                    'away_goals': 'conceded_goals'})
        df_home_matches['home?'] = 'yes'

        df_away_matches = df[df['away_team'] == team]
        df_away_matches = df_away_matches.drop(columns=['away_team'])
        df_away_matches = df_away_matches.rename(columns={'home_team': 'team', 
                                                    'away_goals': 'made_goals', 
                                                    'home_goals': 'conceded_goals'})
        df_away_matches = df_away_matches[['team',
                                    'made_goals',
                                    'conceded_goals',
                                    'result',
                                    'season']]
        df_away_matches['home?'] = 'no'



        df_team = pd.concat([df_home_matches, df_away_matches])
        df_team['goal_diff'] = df_team['made_goals'] - df_team['conceded_goals'] 

        return df_team.sort_index()

    #TODO: Write proper input and output format
    def make_team_vs_team_data(self):
        """

        """
        pass

    def df2jason(self):
        pass

    def get_team_data(self):
        """
        
        """
        # TODO: Make so this returns directly from dict if exist
        #   otherwise use make_team_data to make data
        pass

        
    def get_team_vs_team_data(self):
        """
        
        """
        # TODO: Make so this returns directly from dict if exist
        #   otherwise use make_team_vs_team_data to make data
        pass