from flask import Flask, jsonify, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
from dotenv import load_dotenv 
from forms import RegistrationForm, LoginForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('secret_cookie_key')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title= 'Register' ,form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title = 'Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)




        