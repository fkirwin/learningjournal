from flask import Flask, g, render_template, flash, redirect, url_for, abort
from flask_bcrypt import check_password_hash, Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import models
import forms

##Default variables
PORT = 8080
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

@app.route("/entries")
@app.route("/")
def entries():
    entriez = models.Entry.select()
    return render_template("index.html", entriez=entriez)

@app.route("/entries/<entry_id>")
def specific_entry(entry_id):
    entry = models.Entry.select().where(models.Entry.id == entry_id).get()
    return render_template("detail.html", entry=entry)

@app.route("/entries/edit/<entry_id>", methods=("GET", "POST"))
def edit(entry_id):
    entry = models.Entry.select().where(models.Entry.id == entry_id).get()
    form = forms.EntryForm()
    if form.validate_on_submit():
        entry.update(title = form.title.data,
                     date = form.date.data,
                     time_spent = form.time_spent.data,
                     learnings = form.learnings.data,
                     rememberings = form.rememberings.data)
        flash("Entry updated! Thanks!", "success")
        return redirect(url_for('entries'))
    return render_template("edit.html", entry=entry, form=form)

@app.route("/entries/delete/<entry_id>", methods=["POST"])
def delete(entry_id):
    pass

@app.route("/new", methods=("GET", "POST"))
def new():
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.DATABASE.connect()
        models.Entry.write_entry(user=models.User.get(models.User.id==1),
                                 title = form.title.data,
                                 date = form.date.data,
                                 time_spent = form.time_spent.data,
                                 learnings = form.learnings.data,
                                 rememberings = form.rememberings.data)
        models.DATABASE.close()
        flash("New entry created!", "success")
        return redirect(url_for('entries'))
    return render_template("new.html", form=form)

if __name__ == '__main__':
    models.initialize()
    app.run(host=HOST, port=PORT)