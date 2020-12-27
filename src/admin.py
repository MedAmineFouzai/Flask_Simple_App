from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from models import (db,User)

admin = Admin(None, name='Admin', index_view= AdminIndexView(
            name='Home',
             template='home.html',
            url='/'
        ),template_mode='bootstrap3')
        
admin.add_view(ModelView(User, db.session))
