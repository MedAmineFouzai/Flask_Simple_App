from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password=db.Column(db.String(200), unique=False, nullable=False)
    is_admin=db.Column(db.Boolean, unique=False, nullable=False)
    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)

class Product(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), unique=False, nullable=False)
    product_price = db.Column(db.String(200), unique=False, nullable=False)
    product_image= db.Column(db.String(200),unique=False,nullable=False)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categories.id',onupdate="CASCADE",ondelete='CASCADE'),nullable=False)


class Categorie(db.Model):
    __tablename__="categories"
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    categorie_name = db.Column(db.String(200), unique=True,nullable=False)
