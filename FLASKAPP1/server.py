from flask import Flask, redirect, url_for, render_template, request, session
import mysql.connector
import re

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  
)
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS testdb")
mycursor.execute("USE testdb")
mycursor.execute("CREATE TABLE IF NOT EXISTS accounts (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,fullname VARCHAR(255) NOT NULL,username VARCHAR(255) NOT NULL,password VARCHAR(255) NOT NULL,email VARCHAR(255) NOT NULL)")
app = Flask(__name__,template_folder='template')

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'team13'

# http://localhost:5000/pythonlogin/ - this will be the login page
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
 # connect

  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        mycursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = mycursor.fetchone()
   
    # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('hello_name'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
    return render_template('login.html', msg=msg)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mysql",
  database="testdb"
)
mycursor = mydb.cursor()

@app.route('/register', methods =['GET', 'POST']) 
def register(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        fullname = request.form['fullname']
        username = request.form['username'] 
        password = request.form['password'] 
        email = request.form['email']  
        mycursor.execute('SELECT * FROM accounts WHERE username = %s', (username, )) 
        account = mycursor.fetchone() 
        if account: 
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email: 
            msg = 'Please fill out the form !'
        else: 
            #mycursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s)', (fullname, username, password, email))
            sql = 'INSERT INTO accounts (id, fullname, username, password, email) VALUES (NULL, %s, %s, %s, %s)'
            val = (fullname, username, password, email)

            mycursor.execute(sql, val)
            mydb.commit() 
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)    

# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('hello_name'))    
       
# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile(): 
 # Check if account exists using MySQL
  
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        mycursor.execute('SELECT * FROM accounts WHERE id = %s', [session['id']])
        account = mycursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('hello_name'))


@app.route('/')
def hello_name():
   return render_template('index.html', username=session['username'])

@app.route('/adddoctor')
def adddoctor():
   return render_template('adddoctor.html')

@app.route('/viewdoctor')
def viewdoctor():
   return render_template('viewdoctor.html')

@app.route('/addpatient')
def addpatient():
   return render_template('addpatient.html')

@app.route('/viewpatient')
def viewpatient():
   return render_template('viewpatient.html')

@app.route('/addnurse')
def addnurse():
   return render_template('addnurse.html')

@app.route('/viewnurse')
def viewnurse():
   return render_template('viewnurse.html')

@app.route('/addsession')
def addsession():
   return render_template('addsession.html')

@app.route('/viewsession')
def viewsession():
   return render_template('viewsession.html')

if __name__ == '__main__':
   app.run()

   