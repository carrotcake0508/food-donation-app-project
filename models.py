from datetime import datetime
from flask_login import UserMixin
from __init__ import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'donor', 'foodbank', or 'volunteer'
    donations = db.relationship('FoodDonation', backref='donor', lazy=True)

class FoodDonation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)  # e.g., 'kg', 'items', 'boxes'
    expiry_date = db.Column(db.DateTime, nullable=True)
    pickup_address = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='available')  # 'available', 'requested', 'delivered'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    requests = db.relationship('FoodRequest', backref='donation', lazy=True)

class FoodRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donation_id = db.Column(db.Integer, db.ForeignKey('food_donation.id'), nullable=False)
    foodbank_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'completed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)