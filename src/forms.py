from models import (db,Categorie)
from wtforms import (
    Form,
    StringField,
    FileField,
    SelectField,
    DecimalField,
    IntegerField,
    validators)

class ProductForm(Form):
    product_name:str = StringField('Product Name', [validators.required(),validators.Length(min=6, max=25)])
    product_price:int = DecimalField('Product Price', [validators.required(),validators.NumberRange(min=1, max=5)])
    categorie_id:int=SelectField(u'Categories', choices=[])
    product_image:bytes=FileField()
    
class CategorieForm(Form):
    categorie_name:str = StringField('Categorie Name', [validators.required(),validators.Length(min=6, max=35)])