import pandas as pd 
import numpy as np 


class PLData:
    """
    Class that handles data read from Premier league data
    (or other football data on the same format).
    The format that the read csv file needs to have it on the form

        |index|home_team|away_team|home_goals|result|season|,

    which is stored as is in a pandas dataframe, in the attribute .data. 
    Each row represents a match that has been played.

    The attribute team_data also contains a pandas data frame, but data
    for a specific team which is gotten from mangling the .data attribute.
    The format is

        |index|team|made_goals|conceded_goals|result|season|home?|goal_diff|

    and each row represents a match that has been played by the 
    user-choosen team.

    Class also handles transforming some of the data to other forms so that 
    it is plot-able later on in the front-end (module front_end_interaction
    might be needed for convinient use of plotly).

    Attributes .team_name and .opp_team_name indicites which teams the user
    wants to analyse. .team_name is the primary team the user wants to analyse
    (e.g. Chelsea) and .opp_team_name is if the user wants to check stats 
    against a specific opponent, e.g. Chelsea vs Arsenal matches.
    """

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


    def make_team_data(self, team_name):
        """
        Creates data for a specific team, which the user chooses. Format can
        be read in class docstring.
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

        self.team_data = df_team.sort_index()


    def choose_team(self, team_name):
        """
        Sets primary team that user wants to analyse. 
        Needs to be called before get_goal_diffs and choose_opponent_team.
        """
        self.team_name = team_name
        self.make_team_data(team_name)


    def get_goal_diffs(self):
        """
        Gives a pandas series with team names in index and mean goal difference
        as values. Used for creating data for plots
        """
        return self.team_data.groupby('team').mean().goal_diff


    def make_team_vs_team_data(self, opponent_name):
        """
        Creates data for a specific opponent team, which the user chooses,
        i.e., it filters out all matches that are not played against opponent_name
        Format can be read in class docstring.
        """

        self.team_data = self.team_data[self.team_data['team'] == opponent_name]


    def choose_opponent_team(self, opponent_name):
        """
        Sets opponent team that user wants to analyse. 
        Needs to be called before get_scatter_goal_data
        and choose_opponent_team needs to be called before this funciton.
        """

        # Checking if team_name has been inputted by user before this
        if self.team_name:
            self.opp_team_name = opponent_name

            # If user does not want to compare to an opponent team 
            #   then team_data should be for all opponent teams possible
            if opponent_name == 'No team':
                self.make_team_data(self.team_name)
            else:
                self.make_team_vs_team_data(opponent_name)


    def get_scatter_goal_data(self, bubble_size = 5):
        """
        Returns data for scatter plot of goals made vs goals .
        Made goals is in attribute .y and conceded goals in 
        attribute .x .  
        """

        df_pairs = self.team_data.groupby(['made_goals', 'conceded_goals']).size()
        y = df_pairs.index.labels[0].values()
        x = df_pairs.index.labels[1].values()

        # freq holds how many matches have been played with those end results
        freq = df_pairs.values

        # Dynamic sizing of bubbles in bubble chart, so that a lot of matches
        # played is comparable to only a few matches played visually
        bubble_sizes = (bubble_size*freq/freq.max()) ** 2

        return pd.DataFrame({'x':x, 'y': y, 'bubble_sizes':bubble_sizes})


    def get_team_choices(self):
        """
        Returns list of tuples for SelectField
        in flask. These are the choices that the user will be
        able to choose, and every choice has 
        the same name/string as in the dataframe self.team_data.

        Returns list of tuples, e.g. [('team_1', 'team_1'), ('team_2','team_2'), ...]
        were first item in each tuple is what back-end recieves as answer,
        and the second is what the user sees
        """

        # Checks both home and away matches, in case of the data being
        # incomplete. If data complete, all team choices shoudl be present
        # in either of those columns
        home_teams = self.data['home_team'].unique()
        away_teams = self.data['away_team'].unique()

        all_teams = np.concatenate((home_teams, away_teams))
        all_teams = np.unique(all_teams)
        
        choices = []
        for team in all_teams:
            choices.append((team, team))
        
        return choices


    def get_opp_team_choices(self):
        """
        Returns list of tuples for SelectField
        in flask. These are the choices that the user will be
        able to choose, and every choice has 
        the same name/string as in the dataframe self.team_data.

        Returns list of tuples, e.g. [('team_1', 'team_1'), ('team_2','team_2'), ...]
        were first item in each tuple is what back-end recieves as answer,
        and the second is what the user sees.

        Sets one choice as ('No team', 'No team') so that the user gets
        an option not to choose an opponent team, i.e. see stats
        for all teams the the primary team have met
        """

        opp_teams = self.team_data['team'].unique()

        choices = [('No team', 'No team')]
        for team in opp_teams:
            choices.append((team, team))

        return choices
        
        

        
