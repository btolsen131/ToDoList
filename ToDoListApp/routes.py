from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from ToDoListApp import app, db, bcrypt, mail
from ToDoListApp.forms import NewTask, RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from ToDoListApp.database_models import User, Post
from flask_mail import Message
from boto.s3.connection import S3Connection
import os

appName='Do It Already'

@app.route('/', methods=['GET', 'POST'])
def log_in():
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
            flash('Login failed. Please check your email and password.', 'danger')
    return render_template('login.html',
                            the_title = appName, form = form)

#profile page
@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    task_list = Post.query.filter_by(user_id=int(current_user.id))
    return render_template('profile.html',
                            the_title= appName,
                            task_list = task_list)

#page for individual tasks
@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',
                            title = post.title,
                            post = post)

#update posts
@app.route('/post/<int:post_id>/update', methods=['GET','POST'])
@login_required
def update_task(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = NewTask()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content =form.content.data
        db.session.commit()
        flash('Your task has been updated accordingly', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_task.html',
                            title = 'Update Task',
                            form = form,
                            legend='Update task')

@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_task(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    flash('Successfully deleted the task!', 'success')
    return redirect(url_for('profile'))


#New task page
@app.route('/profile/new', methods=['GET','POST'])
@login_required
def new_post():
    form = NewTask()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author= current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your task has been created','success')
        return redirect(url_for('profile'))

    return render_template('create_task.html',
                            title = 'New Task',
                            form = form,
                            legend = 'New Task')

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
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('log_in'))

    return render_template('register.html', title='Register', form = form)

#logout
@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out of your account.', 'warning')
    return redirect(url_for('log_in'))

#function to send email for password reset
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request: Just Do It Already',
                sender= str(S3Connection(os.environ['AdminEmail'])),
                recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external = True)}
If you didn't make this request, please disregard.
                '''
    mail.send(msg)

#requesting to reset password
@app.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to reset your password', 'info')
        return redirect(url_for('log_in'))
    return render_template('reset_request.html', title="Reset Password", form = form)

@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #logging new user info to the database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        #sending newly created user to login screen
        flash('Password has been changed! Please log in.', 'success')
        return redirect(url_for('log_in'))
    return render_template('reset_token.html', title="Reset Password", form = form)
