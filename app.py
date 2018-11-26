from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, SelectField, TextAreaField, PasswordField, validators
from functools import wraps
import pandas as pd
import numpy as np
import json
import plotly
from PLData import PLData
from front_end_interaction import data_to_graph_json


app = Flask(__name__)


# Used for both selecting primary team and selecting opponent team
# field .choices is set dynamically when app is running (later in code)
class TeamForm(Form):
    preset_choices = []
    team = SelectField('Team', choices=preset_choices)


# Index and where the user can choose primary team
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():

    # Data class that stores and handles data for Premier League (PL)
    # init and loads data
    pl_data = PLData(file_name='results.csv')

    # Form for the user to be able to choose which team they want to analyse.
    # e.g. if Chelsea is picked, the data will reflect stats for Chelsea matches
    form = TeamForm(request.form)
    form.team.choices = pl_data.get_team_choices()

    if request.method == 'POST' and form.validate():

        # Redirect for further choices and for graphs
        return redirect(url_for('.team_view', team=form.team.data))
        
    return render_template('home.html', 
                        form=form, 
                        display_tables=False)


# At this route the user first gets the choice if they want to analyse the stats
# against a particular opponent team, and if chosen not to, the user gets
# general data about the chosen primary team
@app.route('/team_view', methods=['GET', 'POST'])
def team_view():

    # Argument 'team' that has been passed in holds the name of the choosen
    # team which the user wants to analyse
    team = request.args['team']

    # Data class that stores and handles data for Premier League (PL)
    # init and loads data
    pl_data = PLData(file_name='results.csv')
    pl_data.choose_team(team)

    # TODO: Make so that user can choose which season they want to see

    # Form for the user to be able to choose which opponent team they want.
    # Opponent team makes the data specific to one opponent,
    # e.g. if Arsenal is picked the data only includes matches between 
    # Arsenal and Chelsea (if Chelsea was pcked as primary team)
    form = TeamForm(request.form)

    # Choices include "No team", so user can choose to look at
    # the primary teams data againt all other teams
    form.team.choices = pl_data.get_opp_team_choices()

    if request.method == 'POST' and form.validate():

        # Does not do anything if no opponent team inputted,
        # i.e. form.opp_team.data is None
        pl_data.choose_opponent_team(form.team.data)

        # Getting data for plots. goal_diffs for first plot
        # and goals_on_matches for second plot 
        goal_diffs = pl_data.get_goal_diffs()
        goals_on_matches = pl_data.get_scatter_goal_data()

        # TODO: Make fields for goals_diffs to .x and .y
        # so it is same format as scatter_data
        graphJSON = data_to_graph_json(goal_diffs, goals_on_matches)

        # display_tables True so that front end knows that it has
        # gotten graph data and can now plot it
        return render_template('team_view.html', 
                                form=form, 
                                team=team,
                                display_tables=True,
                                graphJSON=graphJSON)
        
    # display_tables set to False so that front end knows there is no
    # data to plot
    return render_template('team_view.html', 
                        form=form, 
                        team=team,
                        display_tables=False)


if __name__ == '__main__':
    app.run(debug=True)