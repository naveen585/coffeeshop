from flask import render_template, session, request, redirect, url_for,flash
from shop import app, db, bcrypt
from .forms import SignUpForm, SignInForm
from .models import Customer
from shop.products.models import Product,Category,Brand


@app.route('/admin')
def admin():
    if 'email' not in session:            
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    products= Product.query.all()
    return render_template('admin/index.html', products = products)

@app.route('/brands')
def brands():
    if 'email' not in session:            
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html',brands = brands)


@app.route('/categories')
def categories():
    if 'email' not in session:            
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html',categories = categories)


@app.route('/register',methods=['GET','POST'])
def signup():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        customer = Customer(full_name=form.full_name.data, username=form.username.data, email=form.email.data, password= form.password.data, age = form.age.data)
        db.session.add(customer)
        flash(f'Welcome { form.full_name.data } Thanks for registering','success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('admin/register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm(request.form)
    if request.method == "POST" and form.validate():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user and form.password.data == user.password:
            session['email'] = form.email.data
            flash(f'Welcome {user.username} You are logged now ','success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong Password please try again','danger')

    return render_template('admin/login.html', form = form)