from app import create_app
from app.models import db
import os

app = create_app('DevelopmentConfig')


with app.app_context():
    db.create_all()

app.run(debug=True, port=int(os.environ.get('PORT', 5002)))