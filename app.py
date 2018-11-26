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

    if request.method == 'POST' and form.validate():

        return redirect(url_for('.team_view', team=form.team.data))
        
    return render_template('home.html', 
                        form=form, 
                        display_tables=False)


@app.route('/team_view', methods=['GET', 'POST'])
def team_view():

    team = request.args['team']

    # TODO: Make this db with SQL gets instead
    # Data class that stores and handles data for Premier League (PL)
    #   Init and loads data
    pl_data = PLData(file_name='results.csv')
    pl_data.make_team_data(team)

    # TODO: Make so that if user only specifies one team: use make_team_data
    # Is user specifies team and opponent team, use make_team_vs_team_data
    form = TeamForm(request.form)

    form.team.choices = pl_data.get_opp_team_choices()

    if request.method == 'POST' and form.validate():

        # Does not do anything if no opponent team inputted,
        #   i.e. form.opp_team.data is None
        pl_data.make_team_vs_team_data(form.team.data)

        goal_diffs = pl_data.get_goal_diffs()

        goals_on_matches = pl_data.get_scatter_goal_data()

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
                        x=goals_on_matches.x,
                        y=goals_on_matches.y,
                        type='scatter',                        
                        mode='markers',
                        marker=dict(
                            size=goals_on_matches.bubble_sizes
                        )
                    ),
                ],
                layout=dict(
                    title=form.team.data
                )
            )
        ]

        graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('team_view.html', 
                                form=form, 
                                team=team,
                                display_tables=True,
                                graphJSON=graphJSON)
        
    return render_template('team_view.html', 
                        form=form, 
                        team=team,
                        display_tables=False)


if __name__ == '__main__':
    app.run(debug=True)