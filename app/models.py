from . import db
from flask_login import UserMixin
import datetime
import secrets

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False) 
    campaigns = db.relationship('Campaign', backref='owner', lazy=True)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    token = db.Column(db.String(32), unique=True, nullable=False, default=lambda: secrets.token_hex(16))
    valid_from = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    valid_until = db.Column(db.DateTime, nullable=True)
    questions = db.relationship('Question', backref='campaign', lazy=True)
    responses = db.relationship('Response', backref='campaign', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    guest_identifier = db.Column(db.String(128))
    submitted_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    answers = db.relationship('Answer', backref='response', lazy=True)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey('response.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer_text = db.Column(db.Text)