from flask import Flask, request, redirect, session, render_template
import cloudinary
import cloudinary.uploader

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
import os


app=Flask(__name__)


#Database configuration

DATABASE_URL=os.environ.get("DATABASE_URL")

app.config['SQLALCHEMY_DATABASE_URI'] =DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print(app.config.get('SQLALCHEMY_DATABASE_URI'))
db=SQLAlchemy(app)

app.config['SECRET_KEY'] =os.environ.get("SECRET_KEY")

#Email config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'googlyaqua26@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")


mail=Mail(app)

#cloudinary config
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)

ADMIN_USERNAME = "googlyaqua"
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100))
    requirements = db.Column(db.Text)
    def __repr__(self):
      return f"ContactLead(name={self.name},phone={self.phone} city={self.city}, requirements={self.requirements})"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_message = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))    


    def __repr__(self):
      return f"Review(name={self.name}, rating={self.rating})"



@app.route('/')
def home():
    reviews = Review.query.all()
    return render_template('index.html',reviews=reviews)
    

#lead route    
@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    lead = UserModel(
        name=request.form.get('name'),
        phone=request.form.get('phone'),
        city=request.form.get('city'),
        requirements=request.form.get('requirements')
    )
    db.session.add(lead)
    db.session.commit()
    
    # wrap email in try/except so it doesn't crash the app
    try:
        msg = Message(
            subject='New Lead Received',
            sender=app.config['MAIL_USERNAME'],
            recipients=['googlyaqua26@gmail.com']
        )
        msg.body = f"Name: {lead.name}\nPhone: {lead.phone}\nCity: {lead.city}\nRequirements: {lead.requirements}"
        mail.send(msg)
    except Exception as e:
        print(f"Email failed: {e}")

    return redirect('/')


#Review Route

@app.route('/submit-review', methods=['POST'])
def submit_review():
    name = request.form.get('name')
    rating = request.form.get('rating')
    message = request.form.get('message')
    image_file = request.files.get('review_image')

    image_url = None
    if image_file and image_file.filename != '':
        upload_result = cloudinary.uploader.upload(image_file)
        image_url = upload_result.get('secure_url')

    review = Review(
        name=name,
        rating=int(rating),
        review_message=message,
        image_url=image_url
    )
    db.session.add(review)
    db.session.commit()

    return redirect('/')

#Check Reviews Route
@app.route('/reviews')
def show_reviews():
    reviews = Review.query.all()
    return str([(r.name, r.rating, r.review_message) for r in reviews])



with app.app_context():
   db.create_all()

if __name__=="__main__":
   app.run(debug=True)