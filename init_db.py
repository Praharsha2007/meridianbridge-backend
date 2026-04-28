from app import create_app, db

app = create_app('app.config.DevelopmentConfig')

with app.app_context():
    db.drop_all()
    db.create_all()
    print("✅ Tables recreated successfully!")