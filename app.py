import os

from app import create_app
from app.models import db

app = create_app(os.environ.get('APP_CONFIG', 'DevelopmentConfig'))


with app.app_context():
    #db.drop_all()
    db.create_all()

if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG', False), port=int(os.environ.get('PORT', 5002)))
    
app.run()    