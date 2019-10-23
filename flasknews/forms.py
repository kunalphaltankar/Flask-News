from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flasknews.models import User

class  RegistrationForm(FlaskForm):
	username = StringField('Username',validators = [DataRequired(),Length(min = 2,max = 20)])
	email = StringField('Email',validators = [DataRequired(),Email()])
	password = PasswordField('Password',validators = [DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators = [DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different one.')
		

class  LoginForm(FlaskForm):
	email = StringField('Email',validators = [DataRequired(),Email()])
	password = PasswordField('Password',validators = [DataRequired()])
	remember = BooleanField('Rememeber Me')
	submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken. Please choose a different one.')

class  QueryForm(FlaskForm):
	query_string = StringField("Query",validators=[DataRequired()])
	def on_submit(self,url,title):
		if self.validate_on_submit():
			query = self.query_string.data
			url = 'https://newsapi.org/v2/everything?q=' + query + '&apiKey=afc81dd95663478a88bc39e5cdc851ec'
			title = 'Search results for ' + query
			return (title,url)
		return(title,url)