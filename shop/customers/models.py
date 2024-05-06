from shop import app,db,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return RegistrationDetails.query.get(user_id)

class RegistrationDetails(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    age = db.Column(db.Integer)
    contact = db.Column(db.String(30), unique=False, nullable=False)
    profile = db.Column(db.String(200), unique=False, nullable=False,default='profile.jpg')
    date_created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Register %r>' % self.full_name
    

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.String(30), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(db.Text)

    def __repr__(self):
        return '<CustomerOrder %r>' % self.customer_id

with app.app_context():
    db.create_all()
