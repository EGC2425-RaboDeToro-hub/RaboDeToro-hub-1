from flask_wtf import FlaskForm
from wtforms import SubmitField


class ForgotpasswordForm(FlaskForm):
    submit = SubmitField('Save forgotPassword')
