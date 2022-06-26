from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from market.models import User

class RegisterForm(FlaskForm):  #inheriting FlaskForm
    
    def validate_username(self, username_to_check):  #function named with flask convention
        user = User.query.filter_by(username = username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address = email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Email already exists. Try different Email")
    username = StringField(label="Username:", validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label='Email ID:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()] )
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField('Purchase Item')

class SellItemForm(FlaskForm):
    submit = SubmitField('Sell Item')