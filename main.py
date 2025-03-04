from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm  
from dotenv import load_dotenv
import os
from users import password_to_user, RFID0Corrector, addUser, reload_users_csv
from admin import password_to_admin, reload_admin_csv
import vote
import pandas as pd
import datetime as dt
from logs import logging, checklog

load_dotenv()
RFID0Corrector(password_to_user) # Remove if not using NFC reader
RFID0Corrector(password_to_admin) # Remove if not using NFC reader

votes_file = "csv/votes.csv"
adminfile = "csv/admin.csv"
userfile = "csv/Users.csv"



app = Flask(__name__, template_folder='src/templates', static_folder='src/static')
app.config['SECRET_KEY'] = 'your_secret_key'
LOGS_FOLDER = os.path.join(app.root_path, 'logs')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.is_admin = False

class Admin(UserMixin):
    def __init__(self, username):
        self.id = username
        self.is_admin = True

@login_manager.user_loader
def load_user(user_id):
    if user_id in password_to_user.values():
        return User(user_id)
    elif user_id in password_to_admin.values():
        return Admin(user_id)
    return None

# Define the enumerate filter
@app.template_filter('enumerate')
def enumerate_filter(sequence, start=0):
    return enumerate(sequence, start)

@app.route('/')
@login_required
def home():
    if current_user.is_admin:
        return redirect(url_for('admin'))
    else:
        user_id = current_user.id
        logging(user_id, 'Logged in to home page')
        return render_template('home.html', name=current_user.id)

@app.route('/admin')
@login_required
def admin():
    if current_user.is_admin:
        user_id = current_user.id
        logging(user_id, 'Logged in to admin console')
        return render_template('admin.html', name=current_user.id)
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    users_df = reload_users_csv()
    admin_df = reload_admin_csv()
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
            user = Admin(username)
            login_user(user)
            return redirect(url_for('admin'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html', form=form, users=users_df, admins=admin_df)

@app.route('/logout')
@login_required
def logout():
    user_id = current_user.id
    logging(user_id, 'Logged out')
    logout_user()
    return redirect(url_for('login'))

@app.route('/vote', methods=['GET', 'POST'])
@login_required
def vote_page():
    global votes_df
    if current_user.id in password_to_admin.values():
        if os.path.exists(votes_file):
            votes_df = pd.read_csv(votes_file)
        else:
            votes_df = pd.DataFrame(columns=['user_id', 'choice'])
            votes_df.to_csv(votes_file, index=False)

    if request.method == 'POST':
        data = request.get_json()
        choice = data['choice']
        user_id = current_user.id

        if vote.has_voted(user_id):
            return jsonify(success=False)

        vote.record_vote(user_id, choice)
        return jsonify(success=True)
    
    return render_template('vote.html', name=current_user.id)

@app.route('/view_results')
@login_required
def view_results():
    global votes_df
    user_id = current_user.id
    logging(user_id, 'Viewed results')
    if current_user.id in password_to_admin.values():
        if os.path.exists(votes_file):
            votes_df = pd.read_csv(votes_file)
        else:
            votes_df = pd.DataFrame(columns=['user_id', 'choice'])
            votes_df.to_csv(votes_file, index=False)
        
        if 'choice' in votes_df.columns:
            vote_counts = votes_df['choice'].value_counts().to_dict()
        else:
            vote_counts = {}

        votes = votes_df.to_dict(orient='records')
        return render_template('view.html', votes=votes, vote_counts=vote_counts)
    else:
        return redirect(url_for('unauthorized')) 

@app.route('/download_csv')
@login_required
def download_csv():
    user_id = current_user.id
    logging(user_id, 'Downloaded csv')
    if current_user.id in password_to_admin.values():
        return send_file(votes_file, as_attachment=True, cache_timeout=0)
    else:
        return redirect(url_for('unauthorized'))

@app.route('/delete_csv')
@login_required
def delete_csv():
    user_id = current_user.id
    logging(user_id, 'Deleted csv')
    if current_user.id in password_to_admin.values():
        if os.path.exists(votes_file):
            os.remove(votes_file)
            return redirect(url_for('view_results'))
        else:
            return "No votes.csv file found", 404
    else:
        return redirect(url_for('unauthorized'))

@app.route('/unauthorized')
def unauthorized():
    return render_template('unoth.html'), 403

@app.route('/logs')
@login_required
def list_logs():
    if current_user.get_id() not in password_to_admin.values():
        return redirect(url_for('unauthorized'))
    
    log_files = [f for f in os.listdir(LOGS_FOLDER) if os.path.isfile(os.path.join(LOGS_FOLDER, f))]
    return render_template('list_logs.html', log_files=log_files)

@app.route('/logs/<filename>')
@login_required
def view_log(filename):
    user_id = current_user.id
    logging(user_id,'Opened log file ' + filename)
    if current_user.get_id() not in password_to_admin.values():
        return redirect(url_for('unauthorized'))
    
    if not os.path.isfile(os.path.join(LOGS_FOLDER, filename)):
        return "File not found", 404
    
    with open(os.path.join(LOGS_FOLDER, filename)) as file:
        log_content = file.readlines()
    
    return render_template('view_log.html', filename=filename, log_content=log_content)

@app.route('/logs/download/<filename>')
@login_required
def download_log(filename):
    user_id = current_user.id
    logging(user_id, 'Downloaded log file ' + filename)
    if current_user.get_id() not in password_to_admin.values():
        return redirect(url_for('unauthorized'))
    
    if not os.path.isfile(os.path.join(LOGS_FOLDER, filename)):
        return "File not found", 404
    
    return send_from_directory(LOGS_FOLDER, filename, as_attachment=True)

@app.route('/add_user', methods=['POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        return redirect(url_for('unauthorized')), 403
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        addUser(username, password)
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Invalid data"), 400


if __name__ == '__main__':
    app.run(debug=True)
