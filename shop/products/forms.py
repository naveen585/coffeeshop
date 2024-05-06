from wtforms import (StringField,PasswordField,SubmitField,FloatField,DateTimeField,SelectField,TextField,DecimalField,TextAreaField,IntegerField, validators)
from flask_wtf import Form
from flask_wtf.file import FileAllowed,FileField,FileRequired

class AddProductForm(Form):
    product_name = StringField('Product name ',[validators.DataRequired()])
    product_desc = TextAreaField('Description',[validators.DataRequired()])
    product_price = DecimalField('Price',[validators.DataRequired()])
    product_qty = IntegerField('Quantity',[validators.DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg','png','gif','jpeg']), 'upload images only'])
