# TODO: Rename file 

import pandas as pd 
import numpy as np 

# TODO: Make it a class
class PLData:

    # Pandas dataframes
    data = None 
    team_data = None

    # Strings 
    team_name = None
    opp_team_name = None

    def __init__(self, file_name):

        # All data from file_name
        # File needs to be csv, that is on format *.csv
        self.data = pd.read_csv(file_name)

    # Make so that this constructs team_data. Makes more sense
    def choose_team(self, team_name):
        pass

    # Remember: Make sure to get error when this is used without team specified
    # Or just make it so that it is impossible to input anything else
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
        were first item in each tuple is what back-end recieves as answer,
        and the second is what the user sees
        """

        home_teams = self.data['home_team'].unique()
        away_teams = self.data['home_team'].unique()
        all_teams = np.concatenate((home_teams, away_teams))
        all_teams = np.unique(all_teams)
        
        choices = []
        for team in all_teams:
            choices.append((team, team))
        
        return choices

    def get_opp_team_choices(self):
        """
        Get choices for opponent team
        """
        opp_teams = self.team_data['team'].unique()

        choices = [('No team', 'No team')]

        for team in opp_teams:
            choices.append((team, team))

        return choices
        

    # As for now, this just overwrites exisiting data.
    # Might change when data is stored in db instead 
    # TODO: Make so this does not create make_team_data
    #   if not needed 
    def make_team_vs_team_data(self, opponent_name):
        """

        """
        if self.team_name:
            self.opp_team_name = opponent_name

            # If user does not want to compare to an opponent team 
            #   then team_data should be for all opponent teams possible
            if opponent_name == 'No team':
                self.make_team_data(self.team_name)
                return

            # TODO: Too long line according to PEP
            self.team_data = self.team_data[self.team_data['team'] == opponent_name]


        

    def get_scatter_goal_data(self, bubble_size = 5):
        """
        Returns data for scatter plot of goals made vs goals 
        """

        df_pairs = self.team_data.groupby(['made_goals', 'conceded_goals']).size()
        y = df_pairs.index.labels[0].values()
        x = df_pairs.index.labels[1].values()
        freq = df_pairs.values
        bubble_sizes = (bubble_size*freq/freq.max()) ** 2

        return pd.DataFrame({'x':x, 'y': y, 'bubble_sizes':bubble_sizes})
        

        
