from app import db

class Audience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey("influencer_profile.id"))

    followers = db.Column(db.Integer)
    avg_views = db.Column(db.Integer)

    genres = db.Column(db.JSON)      # ["Tech", "Gaming"]
    languages = db.Column(db.JSON)   # ["English", "Hindi"]