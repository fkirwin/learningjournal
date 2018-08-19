from flask import Flask, g, render_template, flash, redirect, url_for, abort
from flask_bcrypt import check_password_hash, Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import models

##Default variables
PORT = 8000
HOST = '0.0.0.0'

##Application reference.
app = Flask(__name__)
app.secret_key = 'asdf9fs82rnu478200fofj01sksal013rbdabcvbgem2'

##Login manager reference.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

##Bcrypt reference.
bcrypt = Bcrypt(app)

app.route("/")
def index():
    pass

app.route("/entries")
def entries():
    pass

app.route("/entries/<slug>")
def specific_entry(slug):
    pass

app.route("/entries/edit/<slug>")
def edit(slug):
    pass

app.route("/entries/delete/<slug>")
def delete(slug):
    pass

if __name__ == '__main__':
    models.initialize()
    app.run(host=HOST, port=PORT)