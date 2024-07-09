from flask import Flask, render_template, redirect, url_for, request, jsonify, Response, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm  
from dotenv import load_dotenv
import os
from users import password_to_user, RFID0Corrector
from admin import password_to_admin
import vote
import pandas as pd


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

votes_file = "votes.csv"
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

@app.route('/vote', methods=['GET', 'POST'])
@login_required
def vote_page():
    global votes_df
    if current_user.id in password_to_admin.values():
        if os.path.exists(votes_file):
            votes_df = pd.read_csv(votes_file)
        else:
            votes_df = pd.DataFrame(columns=['user_id', 'choice'])

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
    
    if current_user.id in password_to_admin.values():
        # Read vote.csv on each request to get the latest data
        if os.path.exists('votes.csv'):
            votes_df = pd.read_csv('votes.csv')
        else:
            votes_df = pd.DataFrame(columns=['user_id', 'choice'])
        
        # Calculate vote counts
        vote_counts = votes_df['choice'].value_counts().to_dict()

        votes = votes_df.to_dict(orient='records')
        return render_template('view.html', votes=votes, vote_counts=vote_counts)
    else:
        return "Unauthorized Access", 403 

@app.route('/download_csv')
@login_required
def download_csv():
    if current_user.id in password_to_admin.values():
        votes_file = 'votes.csv'
        return send_file(votes_file, as_attachment=True, cache_timeout=0)
    else:
        return "Unauthorized Access", 403

@app.route('/delete_csv')
@login_required
def delete_csv():
    if current_user.id in password_to_admin.values():
        if os.path.exists(votes_file):
            os.remove(votes_file)
            return redirect(url_for('view_results'))
        else:
            return "No votes.csv file found", 404
    else:
        return "Unauthorized Access", 403

if __name__ == '__main__':
    app.run(debug=True)
