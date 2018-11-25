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

    choices = pl_data.get_team_choices()

    # TODO: Make so that if user only specifies one team: use make_team_data
    # Is user specifies team and opponent team, use make_team_vs_team_data
    form = TeamForm(request.form)

    form.team.choices = choices

    if request.method == 'POST' and form.validate():

        pl_data.make_team_data(form.team.data)

        goal_diffs = pl_data.get_goal_diffs()

        scatter_data = pl_data.get_scatter_goal_data()

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