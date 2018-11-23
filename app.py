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

    form = TeamForm(request.form)

    form.team.choices = choices

    display_tables = False

    # TODO: Validate if team inputted exists
    if request.method == 'POST' and form.validate():

        display_tables = True

        pl_data.make_team_data(form.team.data)


        goal_diffs = pl_data.get_goal_diffs()

        graphs = dict(data=[
                    dict(
                        x=goal_diffs.index,
                        y=goal_diffs,
                        type='bar'
                    ),
                    ],
                    layout=dict(
                        title='Team name'
                    )
        )

        graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
            
        # TODO: Scatter plot for goals vs concated goals
        
        return render_template('home.html', 
                                form=form, 
                                display_tables=display_tables,
                                graphJSON=graphJSON)
        
    return render_template('home.html', 
                        form=form, 
                        display_tables=display_tables)


if __name__ == '__main__':
    app.run(debug=True)