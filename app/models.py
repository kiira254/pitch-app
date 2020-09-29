from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime, timezone, time, timedelta,timezone
# import pytz

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Pitch(db.Model):
    __tablename__='pitch'
    id=db.Column(db.Integer,primary_key=True)
    pitch=db.Column(db.String())
    pitch_category=db.Column(db.String(20))
    posted=db.Column(db.DateTime,default=datetime.utcnow)
    upvotes=db.Column(db.Integer)
    downvotes=db.Column(db.Integer)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username=db.Column(db.String(255),unique=True,nullable=False)
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash=db.Column(db.String(255))
    bio=db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    comment=db.relationship('Comment',backref='user',lazy='dynamic')
    pitch=db.relationship('Pitch',backref='user',lazy='dynamic')
    password_secure = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot access the password')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.pitch}')"

class Comment(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer,primary_key=True)
    comment=db.Column(db.String)
    posted=db.Column(db.DateTime,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    pitch_id=db.Column(db.Integer,db.ForeignKey('pitch.id'))


    def __repr__(self):
        return f"Comment ('{self.comment}','{self.user}')"
        
    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,pitch_id):
        comment=Comment.query.filter_by(pitch_id=pitch_id).all()
        return comment

class Votes(db.Model):
    __tablename__='votes'

    id = db.Column(db. Integer, primary_key=True)
    vote = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_vote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_votes(cls,user_id,pitches_id):
        votes = Votes.query.filter_by(user_id=user_id, pitches_id=id).all()
        return votes
    
