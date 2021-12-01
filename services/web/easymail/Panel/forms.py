from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,IntegerField, SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo, ValidationError

from easymail.models import User

### Creating submit form for searching keywords ###
class SearchForm(FlaskForm):
    keyword = StringField('Keyword',validators=[DataRequired()])
    number_of_links = IntegerField('Number',validators=[DataRequired()])
    country = SelectField('Country',choices=[('pl','Poland'),('en','England')])
    submit = SubmitField('Search')