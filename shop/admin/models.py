from shop import db
from shop import app

class Customer(db.Model):
    __tablename__="customer"
    
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    age = db.Column(db.Integer)

    def __init__(self,full_name,username,email,password,age):
        self.full_name = full_name
        self.username = username
        self.email = email
        self.password = password
        self.age = age
    
    def __repr__(self):
        return f"Customer {self.full_name}, {self.username}, {self.email}, {self.password}, {self.age}"


with app.app_context():
    db.create_all()