from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from flask_mysqldb import MySQL
from wtforms import Form, StringField, SelectField, TextAreaField, PasswordField, validators
#from passlib.hash import sha256_crypt
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

    # TODO: Make this not load everytime. Preferably a db, I guess
    # Load data
    all_data = pd.read_csv('results.csv')

    # Data class that stores and handles data for Premier League (PL)
    pl_data = PLData(file_name='results.csv')

    # TODO: Make choices form pl_data (unique teams)
    choices = [('Chelsea', 'Chelsea'), ('Arsenal', 'Arsenal')]


    # TODO: Make this "rullgardin" with options from data above
    form = TeamForm(request.form)

    form.team.choices = choices

    display_tables = False

    # TODO: Validate if team inputted exists
    if request.method == 'POST' and form.validate():

        display_tables = True

        # TODO: Choice of team set by user
        pl_data.make_team_data('Chelsea')

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
            
        return render_template('home.html', 
                                form=form, 
                                display_tables=display_tables,
                                graphJSON=graphJSON)
        
        print('Worked')
    return render_template('home.html', 
                        form=form, 
                        display_tables=display_tables)

# results
@app.route('/results', methods=['GET', 'POST'])
def results():

    return render_template('results.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')

""" # Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)
 """

""" # User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')
 """

""" # Dashboard
@app.route('/dashboard')
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    #result = cur.execute("SELECT * FROM articles")
    # Show articles only from the user logged in 
    result = cur.execute("SELECT * FROM articles WHERE author = %s", [session['username']])

    articles = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()
 """
"""
# Article Form Class
class TeamForm(Form):
    team = StringField('Team', [validators.Length(min=1, max=200)])
    
# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Article Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)
"""

if __name__ == '__main__':
    app.run(debug=True)