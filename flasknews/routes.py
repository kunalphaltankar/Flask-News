import os
import secrets
from PIL import Image
import requests
from flask import render_template, url_for, flash, redirect, request
from flasknews.forms import RegistrationForm, LoginForm, UpdateAccountForm, QueryForm
from flasknews import app, bcrypt, db
from flasknews.models import User
from flask_login import login_user, current_user, logout_user, login_required






#Test Cases
@app.route("/test_var_access", methods = ['GET', 'POST'])
def test_var_access():
	value = request.values.get("link")
	if value:
		print(value)
	return render_template('test_var_access.html')


# Basic Info
@app.route("/", methods = ['GET', 'POST'])
@app.route("/home")
def home():
	url = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=afc81dd95663478a88bc39e5cdc851ec'
	form = QueryForm()
	title = 'Home'
	(title,url) = form.on_submit(url,title)
	
	response = requests.get(url)
	news = response.json()
	return render_template('home.html',news = news, title = title, form = form)

@app.route("/about")
def about():
	return render_template('about.html', title = 'About Us')

@app.route("/news")
def newsDict():
	url = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=afc81dd95663478a88bc39e5cdc851ec'
	response = requests.get(url)
	news = response.json()
	return news

# Register/Login/Account Information

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username = form.username.data,email = form.email.data,password = hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created! Now You Can Login!','success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user,remember = form.remember.data)
			next_page = request.args.get('next')
			flash('You have been logged in!', 'success')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account',image_file=image_file, form=form)

# News Categories

@app.route("/entertainment", methods = ['GET', 'POST'])
def entertainment():
	url = ('https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=afc81dd95663478a88bc39e5cdc851ec')
	form = QueryForm()
	title = 'Entertainment'
	(title,url) = form.on_submit(url,title)
	response = requests.get(url)
	news = response.json()
	return render_template('home.html',news = news, title = title, form = form)

@app.route("/business", methods = ['GET', 'POST'])
def business():
	url = ('https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=afc81dd95663478a88bc39e5cdc851ec')
	form = QueryForm()
	title = 'Business'
	(title,url) = form.on_submit(url,title)
	response = requests.get(url)
	news = response.json()
	return render_template('home.html',news = news, title = title, form = form)

@app.route("/general", methods = ['GET', 'POST'])
def general():
	url = ('https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey=afc81dd95663478a88bc39e5cdc851ec')
	form = QueryForm()
	title = 'General'
	(title,url) = form.on_submit(url,title)
	response = requests.get(url)
	news = response.json()
	return render_template('home.html',news = news, title = title, form = form)

@app.route("/health", methods = ['GET', 'POST'])
def health():
	url = ('https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=afc81dd95663478a88bc39e5cdc851ec')
	form = QueryForm()
	title = 'Health'
	(title,url) = form.on_submit(url,title)
	response = requests.get(url)
	news = response.json()
	return render_template('home.html',news = news, title = title, form = form)

@app.route("/science", methods = ['GET', 'POST'])
def science():
	url = ('https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=afc81dd95663478a88bc39e5cdc851ec')
	form = QueryForm()
	title = 'Science'
	(title,url) = form.on_submit(url,title)
	response = requests.get(url)
	news = response.json()
	return render_template('home.html',news = news, title = title, form = form)

@app.route("/sports", methods = ['GET', 'POST'])
def sports():
	url = ('https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=afc81dd95663478a88bc39e5cdc851ec')
	form = QueryForm()
	title = 'Sports'
	(title,url) = form.on_submit(url,title)
	response = requests.get(url)
	news = response.json()
	return render_template('home.html',news = news, title = title, form = form)


@app.route("/technology", methods = ['GET', 'POST'])
def technology():
	url = ('https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=afc81dd95663478a88bc39e5cdc851ec')
	form = QueryForm()
	title = 'Technology'
	(title,url) = form.on_submit(url,title)
	response = requests.get(url)
	news = response.json()
	return render_template('home.html',news = news, title = title, form = form)
