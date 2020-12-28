import sys 
sys.path.insert(1,"./src/")
from views import app,login_manager
from admin import admin
from models import db
from config import init_config_app

app=init_config_app(app)
login_manager.init_app(app)
db.init_app(app=app)
admin.init_app(app=app)

if __name__ == "__main__":
    app.run()

