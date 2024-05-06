from flask import render_template, session, request, redirect, url_for,flash,current_app
from shop import app, db,photos
from .models import Brand, Category, Product
from .forms import AddProductForm
import secrets,os

@app.route('/')
def home():
    products = Product.query.filter(Product.product_qty >0)
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    print(brands)
    return render_template('products/index.html', products = products,brands =brands,categories=categories)

@app.route('/product/<int:id>')
def single_page(id):
    product = Product.query.get_or_404(id)
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    return render_template('products/single_page.html',product=product,brands=brands,categories=categories)

@app.route('/brand/<int:id>')
def get_brand(id):
    brand = Product.query.filter_by(brand_id=id)
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    return render_template('products/index.html', brand = brand,brands = brands,categories =categories)

@app.route('/categories/<int:id>')
def get_category(id):
    get_cat = Product.query.filter_by(category_id = id)
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    return render_template('products/index.html',get_cat = get_cat,categories=categories,brands=brands)

@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if 'email' not in session:            
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} has been added successfully','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html',brands='brands')

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:            
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method=="POST":
        updatebrand.name= brand
        flash(f'Brand updated successfully','success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html',updatebrand=updatebrand)

@app.route('/deletebrand/<int:id>', methods=['GET','POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    db.session.delete(brand)
    db.session.commit()
    flash(f'Brand {brand.name} has been deleted successfully','success')
    return redirect(url_for('admin'))

@app.route('/addcategory', methods=['GET','POST'])
def addcategory():
    if 'email' not in session:            
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        flash(f'The Category {getcategory} has been added successfully','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html')

@app.route('/updatecategory/<int:id>',methods=['GET','POST'])
def updatecategory(id):
    if 'email' not in session:            
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method=="POST":
        updatecategory.name= category
        flash(f'Category updated successfully','success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/updatebrand.html',updatecategory=updatecategory)

@app.route('/deletecategory/<int:id>',methods=['GET','POST'])
def deletecategory(id):
    print('inside ')
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash(f'Category {category.name} has been deleted successfully','success')
    return redirect(url_for('admin'))

@app.route('/addproduct', methods=['GET','POST'])
def addprodcut():
    if 'email' not in session:            
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProductForm(request.form)
    if request.method =="POST":
        product_name=form.product_name.data
        product_desc=form.product_desc.data
        product_price=form.product_price.data
        product_qty=form.product_qty.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image =photos.save(request.files.get('image'), name=secrets.token_hex(10)+".")
        addproduct = Product(product_name=product_name,product_desc=product_desc,product_price=product_price,product_qty=product_qty,
                            image = image,brand_id= brand,category_id= category)
        db.session.add(addproduct)
        db.session.commit()
        flash(f'The product {product_name} has been added.','success')
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html',form=form, brands = brands, categories = categories)

@app.route('/updateproduct/<int:id>',methods=['GET','POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Product.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = AddProductForm(request.form)
    if request.method=="POST":
        product.product_name=form.product_name.data
        product.product_desc=form.product_desc.data
        product.product_price=form.product_price.data
        product.product_qty=form.product_qty.data
        product.brand_id = brand
        product.category_id = category
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image))
                product.image = photos.save(request.files.get('image'), name=secrets.token_hex(10)+".")
            except:
                product.image = photos.save(request.files.get('image'), name=secrets.token_hex(10)+".")
        db.session.commit()
        flash(f'Product updated successfully','success')
        return redirect('/admin')
    form.product_name.data = product.product_name
    form.product_desc.data = product.product_desc
    form.product_price.data = product.product_price
    form.product_qty.data = product.product_qty
    return render_template('products/updateproduct.html',form = form, brands = brands,categories=categories,product=product)

@app.route('/deleteproduct/<int:id>', methods=['GET','POST'])
def deleteproduct(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash(f'Product {product.product_name} has been deleted successfully','success')
    return redirect(url_for('admin'))