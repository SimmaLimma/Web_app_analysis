from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, SelectField, TextAreaField, PasswordField, validators
from functools import wraps
import pandas as pd
import numpy as np
import json
import plotly
from PLFuncs import PLData


app = Flask(__name__)

# TODO: Fix validator
# Team Form Class
class TeamForm(Form):
    preset_choices = []
    # TODO: Set validator as DataRequired
    team = SelectField('Team', choices=preset_choices)
    
class OppTeamForm(Form):
    preset_choices_opp = [(None, 'No teams found')]
    opp_team = SelectField('Opponent team', choices=preset_choices_opp)
    


# Index
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():

    # TODO: Make this db with SQL gets instead
    # Data class that stores and handles data for Premier League (PL)
    #   Init and loads data
    pl_data = PLData(file_name='results.csv')

    # TODO: Make so that if user only specifies one team: use make_team_data
    # Is user specifies team and opponent team, use make_team_vs_team_data
    form = TeamForm(request.form)

    form.team.choices = pl_data.get_team_choices()

    if request.method == 'POST': #and form.validate():

        pl_data.make_team_data(form.team.data)

        # TODO: When choosing new team, make opp_team reset (including is the UI)
        form.opp_team.choices = pl_data.get_opp_team_choices()

        # Does not do anything if no opponent team inputted,
        #   i.e. form.opp_team.data is None
        pl_data.make_team_vs_team_data(form.opp_team.data)

        goal_diffs = pl_data.get_goal_diffs()

        scatter_data = pl_data.get_scatter_goal_data()

        # TODO: Make fields for goals_diffs to .x and .y
        #   so it is same format as scatter_data
        graphs = [
            dict(
                data=[
                    dict(
                        x=goal_diffs.index,
                        y=goal_diffs,
                        type='bar'
                    ),
                ],
                layout=dict(
                    title=form.team.data
                )
            ), 
            dict(
                data=[
                    dict(
                        x=scatter_data.x,
                        y=scatter_data.y,
                        type='scatter',                        
                        mode='markers',
                        marker=dict(
                            size=scatter_data.bubble_sizes
                        )
                    ),
                ],
                layout=dict(
                    title=form.team.data
                )
            )
        ]

        graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('home.html', 
                                form=form, 
                                display_tables=True,
                                graphJSON=graphJSON)
        
    return render_template('home.html', 
                        form=form, 
                        display_tables=False)


if __name__ == '__main__':
    app.run(debug=True)