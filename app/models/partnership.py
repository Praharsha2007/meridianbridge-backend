from app import db

class Partnership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey("influencer_profile.id"))

    experience = db.Column(db.String(50))  # none / occasional / regular
    fee = db.Column(db.Integer)

    categories = db.Column(db.JSON)  # ["Fashion", "Tech"]
    long_term = db.Column(db.Boolean)