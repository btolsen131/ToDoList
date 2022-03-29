from flask import Flask, render_template, request, session, redirect, url_for, g 

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
            return redirect(url_for('profile'))
        #send back to     
        return redirect(url_for('log_in'))

    return render_template('login.html',
                            the_title = appName)

@app.route('/profile')
def profile()-> 'html':
    return render_template('profile.html',
                            the_title= appName)   

app.secret_key = 'todoornottodo'

if __name__=='__main__':
    app.run(debug=True)

