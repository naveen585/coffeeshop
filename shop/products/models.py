from shop import db,app

class Product(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String(80), nullable= False)
    product_desc = db.Column(db.Text, nullable= False)
    product_price = db.Column(db.Numeric(10,2),nullable=False)
    product_qty = db.Column(db.Integer, nullable=False)
    brand_id= db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand',backref=db.backref('brands',lazy=True))

    category_id= db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category',backref=db.backref('categories',lazy=True))

    image = db.Column(db.String(150),nullable=False)
    
    def __repr__(self):
        return '<Product %r>' % self.name

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Brand %r>' % self.name
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Catgory %r>' % self.name


with app.app_context():
    db.create_all()