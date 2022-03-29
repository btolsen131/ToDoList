from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)   

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
    def __repr__(self) -> str:
        pass

users = []
users.append(User(id=1, username='Tony', password ='password'))

appName = "Do it already"

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET','POST'])
def log_in() -> 'html':
    if request.method == 'POST':
        session.pop('user_id', None)

        #get passed in username and password
        username = request.form['username']
        password = request.form['password']

        #check if username is in users list
        user =[x for x in users if x.username == username][0]

        #if the passwords match redirect to the persons profile
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        #send back to     
        return redirect(url_for('login'))



    return render_template('login.html',
                            the_title = appName)

@app.route('/profile')
def show_list()-> 'html':
    pass

if __name__=='__main__':
    app.run(debug=True)

