from flask import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField,
                     SelectField, IntegerField, TextAreaField)
from wtforms.fields.html5 import EmailField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Regexp
from wtforms import ValidationError
from datetime import datetime
from app import usi


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


class EventForm(FlaskForm):
    """
    Form for creating events.

    """
    title = StringField('Title', validators=[
        DataRequired('Event tile is required.')])
    description = TextAreaField('Description')
    address = StringField('Address')
    start_date = DateField('Start Date', validators=[
        DataRequired('Event start date is required.')])
    end_date = DateField('End Date', validators=[
        DataRequired('Event end date is required.')])
    start_time = TimeField('Start time', validators=[
        DataRequired('Event start time is required.')])
    end_time = TimeField('End time', validators=[
        DataRequired('Event end time is required.')])
    travel_method = SelectField('Travel Method', choices=[
        ('walk', 'Walk'), ('driving', 'Drive'),
        ('transit', 'Public Transport'), ('bicycling', 'Bike')])
    submit = SubmitField('Create Event')

    def validate(self):
        # Get result of other validations
        res = super(EventForm, self).validate()
        # Check that times are valid
        start_datetime = datetime.combine(
            self.start_date.data, self.start_time.data)
        end_datetime = datetime.combine(
            self.end_date.data, self.end_time.data)
        if start_datetime > end_datetime:
            self.end_time.errors.append("Event cannot start before it ends.")
            res = False
        # Return res
        return res


class ProfileImageForm(FlaskForm):
    """
    Form for uploading profile image.

    """
    image = FileField('Change image', validators=[
        FileRequired(), FileAllowed(['png'], 'PNG files only.')])
    submit = SubmitField('Submit')
