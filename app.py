from flask import Flask, render_template, request, session, redirect, url_for, flash, copy_current_request_context
from checker import check_logged_in
from forms import RegistrationForm, LoginForm
from DBcm import UseDatabase 
from flask_bcrypt import Bcrypt

app = Flask(__name__)   
#setting up database
app.config['dbconfig'] = {'host': '127.0.0.1',
            'user':'root',
            'password': 'fuzzbutt',
            'database': 'do_it_already'}

# Temporary tasks class and objects for testing
class Task:
    def __init__(self, id, task, user_id):
        self.id = id
        self.task = task
        self.user_id = user_id

tasks =[]
tasks.append(Task(id=1,task='Mop the floors',user_id=1))
tasks.append(Task(id=2,task='Vaccum the floors', user_id=1))
tasks.append(Task(id=3,task='clean the pool', user_id=3))

appName = "Do It Already"

@app.route('/', methods=['GET', 'POST'])
def log_in() -> 'html':
    form = LoginForm()
    if form.is_submitted():
        #checking login credentials
        @copy_current_request_context
        def validate_login(req) -> 'redirect':
            with UseDatabase(app.config['dbconfig']) as cursor:
                _SQL = """ SELECT *  
                        FROM login 
                        WHERE email = %s
                        and password = %s """
                cursor.execute(_SQL, (req.form.get('email'),req.form.get('password')))
                login_result = cursor.fetchall()
                print(login_result)
            if not login_result:
                flash(f'Log in failed','fail')
            else:
                print('Great Success!')
                session['logged_in'] = True
                session['user_id'] = login_result[0][0]
                print(session['user_id'])
                #return redirect(url_for('profile'))
        try:
            validate_login(request)
            return redirect(url_for('profile'))
        except Exception as err:
            print('*** Log in failed with the following error: ', str(err))

    return render_template('login.html',
                            the_title = appName, form = form)

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
        
        #logging new user info to the database
        @copy_current_request_context
        def log_new_user(req: 'flask_request'):
            with UseDatabase(app.config['dbconfig']) as cursor:
                _SQL = """insert into login
                        (username, password, email)
                        values
                        (%s,%s,%s)"""
                cursor.execute(_SQL, (req.form.get('username'),
                          req.form.get('password'),
                          req.form.get('email')))
        try:
            log_new_user(request)
        except Exception as err:
            print('*** Logging New User to database failed with the following error: ', str(err))


        #sending newly created user to login screen
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('log_in'))

    return render_template('register.html', title='Register', form = form)
    

app.secret_key = 'secretkeyhassecrets'

if __name__=='__main__':
    app.run(debug=True)

