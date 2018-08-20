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

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('entries'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Registration successful!", "success")
        models.User.write_user(
            username=form.username.data,
            password=form.password.data,
            is_admin=form.is_admin.data
        )
        return redirect(url_for('entries'))
    return render_template('register.html', form=form)


@app.route("/entries")
@app.route("/")
@login_required
def entries():
    entriez = models.Entry.select()
    return render_template("index.html", entriez=entriez)

@app.route("/entries/<entry_id>")
@login_required
def specific_entry(entry_id):
    entry = models.Entry.select().where(models.Entry.id == entry_id).get()
    return render_template("detail.html", entry=entry)

@app.route("/entries/edit/<entry_id>", methods=("GET", "POST"))
@login_required
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
@login_required
def delete(entry_id):
    models.DATABASE.connect()
    with models.DATABASE.transaction():
        target = models.Entry.get(models.Entry.id == entry_id)
        target.delete_instance()
    models.DATABASE.close()
    return redirect(url_for('entries'))

@app.route("/new", methods=("GET", "POST"))
@login_required
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
    app.run(host=HOST, port=PORT, debug=True)