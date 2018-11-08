from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):

    input = StringField(
        'Input', 
        validators=[DataRequired(), Length(min=1, max=30)]
        )

    submit = SubmitField('Search')
