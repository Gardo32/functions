from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm  # Assuming you have a LoginForm defined in forms.py
from dotenv import load_dotenv
import os

load_dotenv()

# Dictionary mapping passwords to usernames
password_to_user = {
    'password_a': 'User A',
    'password_b': 'User B',
    # Add more as needed
}

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock user database
class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    # Load the User object based on the provided username
    return User(user_id)

@app.route('/')
@login_required
def home():
    return render_template('home.html', name=current_user.id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password_attempt = form.password.data
        if password_attempt in password_to_user:
            username = password_to_user[password_attempt]
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/gpa')
@login_required
def gpa():
    return "GPA"

if __name__ == '__main__':
    app.run(debug=True)
