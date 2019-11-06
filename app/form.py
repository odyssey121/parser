from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, URL


class MainForm(FlaskForm):
    site_name = StringField('site_name', validators=[DataRequired(), URL()])
    container_tag = StringField('container_tag', validators=[DataRequired()])
    container_class = StringField('container_class')
    submit = SubmitField('go')
