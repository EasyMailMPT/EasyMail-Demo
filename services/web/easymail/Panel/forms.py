from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,IntegerField, SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo, ValidationError

from easymail.models import User

### Creating submit form for searching keywords ###
class SearchForm(FlaskForm):
    keyword = StringField('Keyword',validators=[DataRequired()])
    number_of_links = IntegerField('Number',validators=[DataRequired()])
    country = SelectField('Country',choices=[('pl','Poland'),('en','England')])
    device = SelectField('Device',choices=[('desktop','Desktop'),('tablet','Tablet'),('mobile','Mobile')])
    domain = SelectField('Domain',choices=[('pl','pl'),('com','com'),('de','de')])
    engine = SelectField('Engine',choices=[('google','Google'),('baidu','Baidu'),('yahoo','Yahoo!')])
    submit = SubmitField('Search')