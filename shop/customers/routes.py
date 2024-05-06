from flask import render_template, session, request, redirect, url_for,flash,current_app
from shop import app, db,photos,login_manager
from flask_login import login_required,current_user,logout_user,login_user
from .forms import CustomerRegistrationForm,CustomerLoginForm
from .models import RegistrationDetails,CustomerOrder

def validate(self, extra_validators=None):
    initial_validation = super(CustomerRegistrationForm, self).validate(extra_validators)

@app.route('/customer/register',methods=['GET','POST'])
def customerregistration():
    form = CustomerRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        registration = RegistrationDetails(full_name = form.full_name.data,username = form.username.data,email = form.email.data,
                                       password = form.password.data,age = form.age.data,contact = form.contact.data)
        db.session.add(registration)
        flash(f'Welcome {form.full_name.data} Thanks for registration','success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)

@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginForm(request.form)
    if form.validate():
        user = RegistrationDetails.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash(f'Logged in','success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Incorrect email and password')
        return redirect(url_for('customerLogin'))
    return render_template('customer/login.html', form=form)

@app.route('/customer/logout')
def customerlogout():
    logout_user()
    return redirect(url_for('customerLogin'))

@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        orders =[]
        for key, item in session['Shoppingcart'].items():
                orders= item['name']
        try:
            order = CustomerOrder(customer_id=customer_id,orders=orders)
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash(f'Your order has been sent','success')
            return render_template('products/orderpage.html')
        except Exception as exception:
            print(exception)
            flash(f'Something went wrong','danger')
            return redirect(url_for('getcart'))

@app.route('/orders')
@login_required
def orders():
    orders = CustomerOrder.query.all()
    return render_template('customer/orders.html',orders=orders)