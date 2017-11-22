from flask import Flask, render_template, redirect, request, session, flash
import re
from mysqlconnection import MySQLConnector

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = MySQLConnector(app, "email_valid")

@app.route('/', methods=['GET'])
def index():
  return render_template("index.html")
@app.route('/process', methods=['POST'])
def submit():
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        return redirect('/')
    else:
        email = "INSERT INTO email (email,created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = { 'email': request.form["email"], }
        mysql.query_db(email,data)
        return redirect('/success')
    

@app.route('/success', methods=['GET'])
def show(): 
	query = "SELECT * FROM email"
	email = mysql.query_db(query)
	return render_template('success.html', all_emails = email)
app.run(debug=True)