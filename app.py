from flask import Flask, render_template, request, session, redirect, url_for, g, flash
from checker import check_logged_in
from forms import RegistrationForm, LoginForm

app = Flask(__name__)   

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Tony', password ='password'))
users.append(User(id=2, username='Marty', password='passwd'))

class Task:
    def __init__(self, id, task, user_id):
        self.id = id
        self.task = task
        self.user_id = user_id

tasks =[]
tasks.append(Task(id=1,task='Mop the floors',user_id=1))
tasks.append(Task(id=2,task='Vaccum the floors', user_id=1))
tasks.append(Task(id=3,task='clean the pool', user_id=2))

appName = "Do it already"

@app.before_first_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user =user

@app.route('/', methods=['GET', 'POST'])
def log_in() -> 'html':
    if request.method == 'POST':
        session.pop('user_id', None)

        #get passed in username and password
        username = request.form['username']
        password = request.form['password']

        #check if username is in users list
        user = [x for x in users if x.username == username]
        user = user[0]
        #if the passwords match redirect to the persons profile
        if user and user.password == password:
            session['user_id'] = user.id
            session['logged_in'] = True
            return redirect(url_for('profile'))
        #send back to     
        return redirect(url_for('log_in'))

    return render_template('login.html',
                            the_title = appName)

@app.route('/profile')
@check_logged_in
def profile()-> 'html':
    tasklist = []
    for task in tasks:
        if task.user_id == session['user_id']:
            tasklist.append(task)

    return render_template('profile.html',
                            the_title= appName,
                            task_list = tasklist)

@app.route('/profile/new', methods=['GET','POST'])
@check_logged_in
def new_post():
    return render_template('create_task.html',
                            title = 'New Post')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.errors)
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('log_in'))

    return render_template('register.html', title='Register', form = form)
    

app.secret_key = 'secretkeyhassecrets'

if __name__=='__main__':
    app.run(debug=True)

