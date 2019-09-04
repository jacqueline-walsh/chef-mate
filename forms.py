from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# registration configuration with validation
class RegistrationForm(FlaskForm):
  firstname = StringField('First Name', validators=[DataRequired()])
  lastname = StringField('Last Name', validators=[DataRequired()])                          
  username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')

# login configuration with validation
class LoginForm(FlaskForm):                    
  username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')                     
  submit = SubmitField('Login')