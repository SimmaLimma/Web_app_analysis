from flask import Flask, render_template
from forms import SearchForm


# Youtube tutorial
# https://www.youtube.com/watch?v=MwZwr5Tvyxo

# Init app
app = Flask(__name__)

# Creating route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    form = SearchForm()
    return render_template('search.html', title='Search', form=form)

if __name__ == '__main__':
    app.run(debug=True)
