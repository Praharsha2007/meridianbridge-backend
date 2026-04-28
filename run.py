from app import create_app
import os

app = create_app('app.config.DevelopmentConfig')

@app.route('/test')
def test():
    db_url = os.environ.get('DATABASE_URL', 'NOT SET')
    return {'DATABASE_URL': db_url[:30]}  # only show first 30 chars for safety

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)