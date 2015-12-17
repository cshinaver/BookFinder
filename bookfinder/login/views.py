from flask import (
    request,
    render_template,
    redirect,
    flash,
)
from flask.ext.login import (
    login_user,
    logout_user,
)
from psycopg2 import IntegrityError

from bookfinder import app, login_manager
from bookfinder.models.bookfinderuser import BookfinderUser as User
from bookfinder.login.forms import LoginForm, CreateUserForm


@app.route('/login/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        form = CreateUserForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            verify_password = form.verify_password.data
            if password == verify_password:
                u = User(username=username, password=password)
                try:
                    u.save()
                except IntegrityError:
                    flash(u'Username already taken', 'error')
                    form = CreateUserForm()
                    return render_template('login/create_user.html', form=form)
                login_user(u)
                flash(u'Welcome {un}'.format(un=username), 'success')
                return redirect('')
            else:
                flash(u'Passwords did not match', 'error')
                return render_template('login/create_user.html', form=form)
    form = CreateUserForm()
    return render_template('login/create_user.html', form=form)


@login_manager.unauthorized_handler
def unauthorized():
    flash('Please login before accessing this page', 'error')
    return login()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            # Authenticate user
            u = User.get(username=username)
            if not u:
                flash('Incorrect Username', 'error')
                return redirect('/login')
            if u.check_password(password):
                login_user(u)
                return redirect('')
            else:
                flash('Incorrect Password', 'error')
                return redirect('/login')

    else:
        form = LoginForm()
        return render_template('login/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('')
