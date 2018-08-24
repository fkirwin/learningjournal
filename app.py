from flask import Flask, g, render_template, flash, redirect, url_for
from flask_bcrypt import check_password_hash, Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import models
import forms

# Default variables
PORT = 8080
HOST = '0.0.0.0'

# Application reference.
app = Flask(__name__)
app.secret_key = 'asdf9fs82rnu478200fofj01sksal013rbdabcvbgem2'

# Login manager reference.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Bcrypt reference.
bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(user_id):
    """Loads user when called."""
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request for connection management."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request for connection management."""
    g.db.close()
    return response


@app.route('/login', methods=('GET', 'POST'))
def login():
    """Core login page for user to enter creds."""
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
    """Core logout page to log the user out."""
    logout_user()
    flash("You've been logged out!", "success")
    return redirect(url_for('login'))


@app.route('/register', methods=('GET', 'POST'))
def register():
    """Create a new user."""
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
    """Landing page for logged in users.  Shows all entries regardless of user."""
    entriez = models.Entry.get_all_entries()
    return render_template("index.html", entriez=entriez)


@app.route("/entries/<entry_id>")
@login_required
def specific_entry(entry_id):
    """Shows details on specific entry."""
    entry = models.Entry.get_specific_entry(entry_id)
    return render_template("detail.html", entry=entry)


@app.route("/entries/edit/<entry_id>", methods=("GET", "POST"))
@login_required
def edit(entry_id):
    """Allows user to edit an entry if they own it."""
    try:
        entry = models.Entry.get_specific_entry_for_user(entry_id, g.user.id)
    except:
        flash("You cannot alter entries you did not write!")
        return redirect(url_for('specific_entry', entry_id=entry_id))
    form = forms.EntryForm()
    if form.validate_on_submit():
        entry.user = g.user.id
        entry.title = form.title.data
        entry.date = form.date.data
        entry.time_spent = form.time_spent.data
        entry.learnings = form.learnings.data
        entry.rememberings = form.rememberings.data
        entry.save()
        flash("Entry updated! Thanks!", "success")
        return redirect(url_for('entries'))
    return render_template("edit.html", entry=entry, form=form)


@app.route("/entries/delete/<entry_id>", methods=["POST"])
@login_required
def delete(entry_id):
    """Allows user to delete entry if they own it."""
    try:
        entry = models.Entry.get_specific_entry_for_user(entry_id, g.user.id)
    except:
        flash("You cannot alter entries you did not write!")
        return redirect(url_for('specific_entry', entry_id=entry_id))
    with models.DATABASE.transaction():
        entry.delete_instance()
    return redirect(url_for('entries'))


@app.route("/new", methods=("GET", "POST"))
@login_required
def new():
    """Allows user to create a new journal entry."""
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.write_entry(user=g.user.id,
                                 title=form.title.data,
                                 date=form.date.data,
                                 time_spent=form.time_spent.data,
                                 learnings=form.learnings.data,
                                 rememberings=form.rememberings.data)
        flash("New entry created!", "success")
        return redirect(url_for('entries'))
    return render_template("new.html", form=form)

if __name__ == '__main__':
    models.initialize()
    app.run(host=HOST, port=PORT, debug=True)
