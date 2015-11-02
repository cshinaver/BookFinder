from flask import request, render_template, abort, redirect
from flask.ext.login import login_user, logout_user

from bookfinder import app
from bookfinder.models.bookfinderuser import BookfinderUser as User
from bookfinder.login.forms import LoginForm


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
                return abort(400)
            if u.check_password(password):
                login_user(u)
                return redirect('')
            else:
                return abort(400)

    else:
        form = LoginForm()
        return render_template('login/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('')
