from flask import (Flask,request,render_template)
from forms import (ProductForm,CategorieForm)
from models import (db,Product,Categorie)
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(Categorie).all()    
    return render_template("Categories/categories.html",categories=categories)

@app.route('/categorie/create', methods=['GET','POST'])
def create_categorie():
    form=CategorieForm(request.form)
    if request.method=="POST":
        categorie=Categorie()
        form.populate_obj(categorie)
        db.session.add(categorie)
        db.session.commit()
        return "OK added"
    return render_template("Categories/addCategorie.html",form=form)

@app.route('/categorie/delete', methods=['GET'])
def delete_categorie():
    print(request.args["id"])
    id=request.args["id"]
    categorie=Categorie.query.filter_by(id=id).first_or_404()
    db.session.delete(categorie)
    db.session.commit()
    return "ok"

@app.route('/products', methods=['GET'])
def get_products():
    products = db.session.query(Product).all()
    return render_template("Products/products.html",products=products)

@app.route('/product/create', methods=['GET','POST'])
def create_product():
    form=ProductForm(request.form)
    form.categorie_id.choices =[(categorie.id,categorie.categorie_name) for categorie in db.session.query(Categorie).all()]
    if request.method=="POST":
        file = request.files[form.product_image.name]
        product=Product()
        form.populate_obj(product)
        product.categorie_id=form.categorie_id.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        product.product_image=filename
        db.session.add(product)
        db.session.commit()
        return "OK added"
    return render_template("Products/addProduct.html",form=form)

@app.route('/product/delete', methods=['GET'])
def delete_product():
    id=request.args["id"]
    product=Product.query.filter_by(id=id).first_or_404()
    db.session.delete(product)
    db.session.commit()
    return "ok deleted"

@app.route('/product/update', methods=['GET','POST'])
def update_product():

    id=request.args["id"]
    product=Product.query.filter_by(id=id).first_or_404()
    selected_categorie=Categorie.query.filter_by(id=product.categorie_id).first_or_404()
    form=ProductForm(request.form)
    categories=db.session.query(Categorie).all()
   
    if request.method=="POST":
        file = request.files["product_image"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        product.product_image=filename
        db.session.query(Product).filter(

			Product.id==id

		).update({
			"product_name":request.form['product_name'],
			"product_price":request.form['product_price'],
            "product_image":filename,
            "categorie_id":request.form.get('categories')
			})
        db.session.commit()
        return "OK added"

    return render_template("Products/updateProduct.html",product=product,
        selected_categorie=selected_categorie,
        categories=categories)