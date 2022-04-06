from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from ToDoListApp import app, db, bcrypt 
from ToDoListApp.forms import NewTask, RegistrationForm, LoginForm
from ToDoListApp.database_models import User, Post

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
            next_page = request.args.get('next')
            #returns user to page they were at prior to logging in, if not it will redirect to the profile page
            return redirect(next_page) if next_page else redirect(url_for('profile'))
        else:
            flash('Login failed. Please check your email and password.')
    return render_template('login.html',
                            the_title = appName, form = form)

#profile page
@app.route('/profile')
@login_required
def profile()-> 'html':
    task_list = Post.query.filter_by(user_id=int(current_user.id))
    print(current_user.id)
    print(task_list)
    return render_template('profile.html',
                            the_title= appName,
                            task_list = task_list)
#New to-do page
@app.route('/profile/new', methods=['GET','POST'])
@login_required
def new_post():
    form = NewTask()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author= current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created','success')
        return redirect(url_for('profile'))

    return render_template('create_task.html',
                            title = 'New Task',
                            form = form)

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