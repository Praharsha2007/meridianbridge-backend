from app import db
from datetime import datetime

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    goal = db.Column(db.String(100))
    platform = db.Column(db.String(50))
    languages = db.Column(db.JSON)

    budget = db.Column(db.String(100))  # changed from Integer to String
    follower_range = db.Column(db.String(50))

    status = db.Column(db.String(50), default="active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)