from flask import Flask
from config import Config
from pyrebase import pyrebase
import os


app = Flask(__name__)

app.config.from_object(Config)

firebaseConfig = {
    'apiKey': "AIzaSyBbOA5oPWYaASy41wQkvKJjQ4vIQajzxuQ",
    'authDomain': "cosmo-juris.firebaseapp.com",
    'databaseURL': "https://cosmo-juris.firebaseio.com",
    'projectId': "cosmo-juris",
    'storageBucket': "cosmo-juris.appspot.com",
    'messagingSenderId': "704825642626",
    'appId': "1:704825642626:web:2e9acae4efdd23b362ee9b",
    'measurementId': "G-41B1JT503R"
}


firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()
# new_user = auth.create_user_with_email_and_password("mintuswaraj1503@gmail.com","Mintu@8472405556")

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/uploads/')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

storage = firebase.storage()

from application import routes

if __name__ == "__main__":
    app.run()