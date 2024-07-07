from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm  # Assuming you have a LoginForm defined in forms.py
from calc import calculate_gpa
from dotenv import load_dotenv
import os
from models import password_to_user, pad_keys_with_zeros

load_dotenv()
pad_keys_with_zeros(password_to_user)

password = os.getenv('password') 


app = Flask(__name__, template_folder='src/templates', static_folder='src/static')
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
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

@app.route('/gpa', methods=['GET', 'POST'])
@login_required
def gpa():
    if request.method == 'POST':
        num_subjects = int(request.form['num_subjects'])
        
        marks_list = []
        hours_list = []
        
        for i in range(num_subjects):
            marks = int(request.form[f'marks_{i+1}'])
            hours = int(request.form[f'hours_{i+1}'])
            marks_list.append(marks)
            hours_list.append(hours)
        
        final_gpa = calculate_gpa(num_subjects, marks_list, hours_list)
        
        return render_template('gpa.html', final_gpa=final_gpa, name=current_user.id, num_subjects=num_subjects)
    
    num_subjects = 0 
    
    return render_template('gpa.html', name=current_user.id, num_subjects=num_subjects)



if __name__ == '__main__':
    app.run(debug=True)
