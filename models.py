# models.py

from main import db  # Adjust import based on your actual module structure

# Define your SQLAlchemy models below
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)

    def __repr__(self):
        return f'<User {self.username}>'
