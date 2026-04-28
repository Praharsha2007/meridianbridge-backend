from app import db

class BrandProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    name = db.Column(db.String(100))
    company_name = db.Column(db.String(150))
    phone = db.Column(db.String(20))