from dotenv import load_dotenv
load_dotenv(verbose=True)
import os

def init_config_app(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")
    app.debug=os.getenv("DEBUG")
    app.secret_key=os.getenv("SECRET_KEY")
    return app
