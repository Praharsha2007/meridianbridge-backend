from app import db

class InfluencerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    full_name = db.Column(db.String(100))
    email = db.Column(db.String(120))

    platform = db.Column(db.String(50))  # Instagram / YouTube
    username = db.Column(db.String(100))
    profile_link = db.Column(db.String(255))

    phone = db.Column(db.String(20))