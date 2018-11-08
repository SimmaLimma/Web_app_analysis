from flask import Flask, render_template


# Youtube tutorial
# https://www.youtube.com/watch?v=MwZwr5Tvyxo

# Init app
app = Flask(__name__)

# Creating route
@app.route('/')
@app.route('/home')
def home():
    return render_template('template.html')

if __name__ == '__main__':
    app.run(debug=True)
