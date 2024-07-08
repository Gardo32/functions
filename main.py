from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm 
from dotenv import load_dotenv
import os
from users import password_to_user
from admin import password_to_admin

load_dotenv()

RFID0Corrector(password_to_user) # Remove if not using NFC reader
RFID0Corrector(password_to_admin) # Remove if not using NFC reader

"""# For testing 
password_to_user = {
    "1234567890": "user1",
    "9876543210": "user2"
}

password_to_admin = {
    "1234567890": "admin1"
}
"""

password = os.getenv('password') 

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.is_admin = username in password_to_admin.values()

@login_manager.user_loader
def load_user(user_id):
    if user_id in password_to_user.values():
        return User(user_id)
    elif user_id in password_to_admin.values():
        return User(user_id)
    return None

@app.route('/')
@login_required
def home():
    return render_template('home.html', name=current_user.id)

@app.route('/admin')
@login_required
def admin():
    if current_user.is_admin:
        return render_template('admin.html', name=current_user.id)
    return redirect(url_for('home'))

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
        elif password_attempt in password_to_admin:
            username = password_to_admin[password_attempt]
            user = User(username)
            login_user(user)
            return redirect(url_for('admin'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
