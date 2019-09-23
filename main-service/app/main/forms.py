from flask import Flask
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     SelectField, IntegerField)
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Length, Regexp
from wtforms import ValidationError
from app import dbi


class UserLoginForm(FlaskForm):
    """
    Form for user registration

    """
    username = StringField('Username', validators=[
        DataRequired('Username is required')])
    password = PasswordField('Password', validators=[
        DataRequired('Password is required')])
    submit = SubmitField('Log In')


class UserRegistrationForm(FlaskForm):
    """
    Form for user registration

    """
    username = StringField('Username', validators=[
        DataRequired('Username is required')])
    password = PasswordField('Password', validators=[
        DataRequired('Password is required')])
    submit = SubmitField('Register')

    def validate(self):
            # Do initial validations
            validation = super(UserRegistrationForm, self).validate()
            # Return false if validations fail
            if validation is False:
                return False
            # Check if username is already taken
            if dbi.getuser(username=self.username.data) is not None:
                # Add error and set valid to false
                self.username.errors.append(
                    "Username is already used by another account")
                validation = False
            # Return whether or not the form was valid
            return validation
