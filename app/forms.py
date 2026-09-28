from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class PredictForm(FlaskForm):
    # Dynamic but fixed top 10 for form
    sp_open = FloatField('SP Open', validators=[DataRequired()])
    sp_close = FloatField('SP Close', validators=[DataRequired()])
    dj_close = FloatField('DJ Close', validators=[DataRequired()])
    eu_price = FloatField('EU Price', validators=[DataRequired()])
    usb_price = FloatField('USB Price', validators=[DataRequired()])
    uso_close = FloatField('USO Close', validators=[DataRequired()])
    gdx_close = FloatField('GDX Close', validators=[DataRequired()])
    # Add 3 more top features
    eu_trend = FloatField('EU Trend', default=1, validators=[Optional()])
    of_trend = FloatField('OF Trend', default=1, validators=[Optional()])
    os_trend = FloatField('OS Trend', default=1, validators=[Optional()])
    submit = SubmitField('Predict Gold Price')

