
  print("Database created successfuly")
from app import app, db

with app.app_context():
  db.create_all()

 
    # IMAGE UPLOAD
