import email
from xml.dom import ValidationErr
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from DBcm import UseDatabase
import mysql.connector

dbconfig = {'host': '127.0.0.1',
            'user':'root',
            'password': 'fuzzbutt',
            'database': 'do_it_already'}


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
        mydb = mysql.connector.connect(**dbconfig)
        mycursor = mydb.cursor()
        _SQL = """ SELECT *
                     FROM login 
                     WHERE username = %s """
        #query database with inputed username
        mycursor.execute(_SQL, (username.data,))
        found_username = mycursor.fetchall()
        if found_username:
            raise ValidationError('Username already exists please select a new one.')
     
    def validate_email(self, email):
        #check if email is in database
        mydb = mysql.connector.connect(**dbconfig)
        mycursor = mydb.cursor()
        _SQL = """ SELECT *
                     FROM login 
                     WHERE email = %s """
        mycursor.execute(_SQL, (email.data,))
        found_email = mycursor.fetchall()
        if found_email:
            raise ValidationError('Email already exists please select a new one or sign into your account.')
    

class LoginForm(FlaskForm):
    email = StringField('Email', 
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                                validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')