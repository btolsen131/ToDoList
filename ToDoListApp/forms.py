from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ToDoListApp.database_models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min =2, max = 20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                                validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        #check if username is in database
        found_user = User.query.filter_by(username=username.data).first()
        if found_user:
            raise ValidationError('Username already exists please select a new one.')
     
    def validate_email(self, email):
        #check if email is in database
        found_email = User.query.filter_by(email=email.data).first()
        if found_email:
            raise ValidationError('Email already exists please select a new one or sign into your account.')
    

class LoginForm(FlaskForm):
    email = StringField('Email', 
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                                validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class NewTask(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    content = TextAreaField('Content',
                        validators=[DataRequired()])
    submit = SubmitField('Add Task')

class RequestResetForm(FlaskForm):
    email = StringField('Email', 
                            validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

    def validate_email(self, email):
        #check if email is in database
        found_email = User.query.filter_by(email=email.data).first()
        if not found_email:
            raise ValidationError('Email not connected to a current account, please register.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                                validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')