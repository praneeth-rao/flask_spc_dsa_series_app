from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'spc-web-app'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(150), unique=True, nullable=False)
  password = db.Column(db.String(150), nullable=False)

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('main'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
      flash('Username already exists!')
      return redirect(url_for('register'))

    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash('Registration successful! Please log in.')
    return redirect(url_for('login'))
  return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
      session['user_id'] = user.id
      session['username'] = user.username
      return redirect(url_for('main'))
    else:
      flash('Invalid credentials. Please try again.')
      return redirect(url_for('leaderboard'))
  return render_template('login.html')

@app.route('/leaderboard')
def leaderboard():
  if 'user_id' not in session:
    flash('Please log in to access this page.')
    return redirect(url_for('login'))
  return render_template('main.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/initdb')
def initdb():
    db.create_all()
    return "Database initialized!"

if __name__ == '__main__':
    app.run(debug=True)
