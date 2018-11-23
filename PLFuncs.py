# TODO: Rename file 

import pandas as pd 
import numpy as np 

# TODO: Make it a class
class PLData:

    data = None
    team_data = None
    team_name = None
    opp_team_name = None

    def __init__(self, file_name):

        # All data from file_name
        # File needs to be csv, that is on format *.csv
        self.data = pd.read_csv(file_name)

    def choose_team(self, team_name):
        pass

    def choose_opponent_team(self, team_name):
        pass

    def make_team_data(self, team_name):
        """

        """

        # TODO: Refactor so that df-search is made as 
        #   "home_team or away_team" == team, in order to skip
        #   unnecessery sort_index and better DRY
        df_home_matches = self.data[self.data['home_team'] == team_name]
        df_home_matches = df_home_matches.drop(columns=['home_team'])
        df_home_matches = df_home_matches.rename(columns={'away_team': 'team', 
                                                    'home_goals': 'made_goals', 
                                                    'away_goals': 'conceded_goals'})
        df_home_matches['home?'] = 'yes'

        df_away_matches = self.data[self.data['away_team'] == team_name]
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

        self.team_name = team_name
        self.team_data = df_team.sort_index()

    def get_goal_diffs(self):
        return self.team_data.groupby('team').mean().goal_diff

    def get_team_choices(self):
        """
        Returns list of tuples for SelectField
        in flask. These are the choices that the user will be
        able to choose, and every user-presentchoice has 
        the same name/string as in the dataframe self.team_data.

        Returns list of tuples, e.g. [('team_1', 'team_1'), ('team_2','team_2'), ...]
        """
        # Remember: Take unique teams from both home and away,
        #   in case of a match is "missing"

        home_teams = self.data['home_team'].unique()
        away_teams = self.data['home_team'].unique()
        all_teams = np.concatenate((home_teams, away_teams))
        all_teams = np.unique(all_teams)
        
        choices = []
        for team in all_teams:
            choices.append((team, team))
        
        return choices


    #TODO: Write proper input and output format
    def make_team_vs_team_data(self):
        """

        """
        pass

    def make_jason(self):
        pass

        #return json-format-data

    def get_team_data(self):
        """
        Unnecessery?
        """
        # TODO: Make so this returns directly from dict if exist
        #   otherwise use make_team_data to make data

        # Do I really need this function?
        pass

        
    def get_team_vs_team_data(self):
        """
        Unnecessery?
        """
        # TODO: Make so this returns directly from dict if exist
        #   otherwise use make_team_vs_team_data to make data

        # Do I really need this function?
        pass