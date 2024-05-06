from flask import render_template, session, request, redirect, url_for,flash,current_app
from shop import app, db
from shop.products.models import Product,Brand,Category




@app.route('/addtocart', methods=['POST'])
def addtocart():
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = Product.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method =="POST":
            DictItems = {product_id:{'name':product.product_name, 'price':product.product_price, 'quantity':product.product_qty, 'image': product.image}}
            if 'Shoppcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                    print("This product in already in cart")
                else:
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as exception:
        print(exception)


@app.route('/carts')
def getcart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    brands = Brand.query.join(Product, (Brand.id == Product.brand_id)).all()
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()
    for key, product in session['Shoppingcart'].items():
        subtotal += float(product['price']) * int(product['quantity'])
        tax = ("%.2f" %(.10 * float(subtotal)))
        grandtotal = float("%.2f" %(1.1 * subtotal))
    return render_template('products/carts.html', tax=tax,grandtotal=grandtotal,brands=brands,categories=categories)


@app.route('/updatecart/<int:code>',methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <=0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash(f'Items updated successfully','success')
                    return redirect(url_for('getcart'))
        except Exception as exception:
            print(exception)
            return redirect(url_for('getcart'))
        
@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <=0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key,None)
                #flash(f'Items updated successfully','success')
                return redirect(url_for('getcart'))
    except Exception as exception:
        print(exception)
        return redirect(url_for('getcart'))
    
@app.route('/clearcart')
def clearcart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as exception:
        print(exception)
