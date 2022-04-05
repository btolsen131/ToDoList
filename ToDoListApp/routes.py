from flask import render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user
from ToDoListApp import app, db, bcrypt 
from ToDoListApp.forms import RegistrationForm, LoginForm
from ToDoListApp.database_models import User, Post
from ToDoListApp.checker import check_logged_in

appName='Do It Already'

@app.route('/', methods=['GET', 'POST'])
def log_in() -> 'html':
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        #checking login credentials
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('profile'))
        else:
            flash('Login failed. Please check your email and password.')
    return render_template('login.html',
                            the_title = appName, form = form)

#profile page
@app.route('/profile')
def profile()-> 'html':
    tasklist=['do the laundry', 'mop the floors']

    return render_template('profile.html',
                            the_title= appName,
                            task_list = tasklist)
#New to-do page
@app.route('/profile/new', methods=['GET','POST'])
def new_post():
    return render_template('create_task.html',
                            title = 'New Post')

#Signup page
@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #logging new user info to the database   
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user =User(username=form.username.data, email = form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        #sending newly created user to login screen
        flash(f'Account created for {form.username.data}! Please log in.', 'success')
        return redirect(url_for('log_in'))

    return render_template('register.html', title='Register', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('log_in'))