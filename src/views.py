from flask import (Flask,request,render_template,redirect)
from flask_login import (LoginManager,login_user,login_required,logout_user)
from forms import (ProductForm,CategorieForm)
from models import (db,Product,Categorie,User)
from collections import Counter
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
import pandas as pd
from math import pi

from werkzeug.utils import secure_filename
import os

app = Flask(__name__,static_folder="static",template_folder='templates')
login_manager=LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first_or_404()
    
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=="POST":
        user=User.query.filter_by(email=request.form['email'],password=request.form['password']).first_or_404()
        if user and user.is_admin==1:
            login_user(user)
            return redirect("/home")
        else:
            return redirect("/login")
    

    return render_template("login.html")

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect("/login")



@app.route('/home', methods=['GET'])
@login_required
def index():
    #bar plot
    pls = ['Products', 'Categories']
    counts=[
            db.session.query(Product).count() if  Exception  else 0, 
            db.session.query(Categorie).count()if  Exception  else 0,
        ]
    chart_colors = ['#484848', '#989898	']
    source = ColumnDataSource(data=dict(pls=pls, counts=counts, color=chart_colors))
    bar_plot = figure(x_range=pls,y_range=(0,9), plot_height=100, title="Statistics",toolbar_location="left")
    bar_plot.vbar(x="pls", top="counts", width=0.9, color='color', legend_field="pls", source=source)
    bar_plot.xgrid.grid_line_color = None
    bar_plot.legend.orientation = "horizontal"
    bar_plot.legend.location = "top_center"
    bar_plot.y_range.start = 0
    bar_plot.plot_width = 500
    bar_plot.plot_height = 400
    
    #pie plot
  
    x=Counter({
            'Product': db.session.query(Product).count()if  Exception  else 0, 
            'Categorie':db.session.query(Categorie).count() if  Exception  else 0,
        })
    data = pd.DataFrame.from_dict(dict(x), orient='index').reset_index().rename(
    index=str, columns={0: 'value', 'index': 'claimNumber'})
    data['angle'] = data['value']/sum(x.values()) * 2*pi
    data['color'] = chart_colors[:len(x)]
    p =  pie = figure(plot_height=350, title="Pie Chart", toolbar_location="left",
           tooltips="@claimNumber: @value", x_range=(-0.5, 1.0))
    p.wedge(x=0, y=1, radius=0.28,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        color='color', legend="claimNumber", source=data)
    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    p.plot_width = 500
    p.plot_height = 300
    pie_plot_script,pie_plot_div=components(p)
    bar_plot_script,bar_plot_div=components(bar_plot)

    return render_template(
        "base.html",
        bar_plot_script=bar_plot_script,
        pie_plot_script=pie_plot_script,
        bar_plot_div=bar_plot_div,
        pie_plot_div=pie_plot_div
        )


@app.route('/categories', methods=['GET'])
@login_required
def get_categories():
    categories = db.session.query(Categorie).all()    
    return render_template("Categories/categories.html",categories=categories)

@app.route('/categorie/create', methods=['GET','POST'])
@login_required
def create_categorie():
    form=CategorieForm(request.form)
    if request.method=="POST":
        categorie=Categorie()
        form.populate_obj(categorie)
        db.session.add(categorie)
        db.session.commit()
        return  redirect("/categories")
    return render_template("Categories/addCategorie.html",form=form)

@app.route('/categorie/delete', methods=['GET'])
@login_required
def delete_categorie():
    print(request.args["id"])
    id=request.args["id"]
    categorie=Categorie.query.filter_by(id=id).first_or_404()
    db.session.delete(categorie)
    db.session.commit()
    return redirect("/categories")

@app.route('/products', methods=['GET'])
@login_required
def get_products():
    products = db.session.query(Product).all()
    return render_template("Products/products.html",products=products)

@app.route('/product/create', methods=['GET','POST'])
@login_required
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
        return  redirect("/products")
    return render_template("Products/addProduct.html",form=form)

@app.route('/product/delete', methods=['GET'])
@login_required
def delete_product():
    id=request.args["id"]
    product=Product.query.filter_by(id=id).first_or_404()
    db.session.delete(product)
    db.session.commit()
    return redirect("/products")

@app.route('/product/update', methods=['GET','POST'])
@login_required
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
        return  redirect("/products")

    return render_template("Products/updateProduct.html",product=product,
        selected_categorie=selected_categorie,
        categories=categories)