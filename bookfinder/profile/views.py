from flask import render_template, redirect, flash
from flask.ext.login import (
    current_user,
    login_required,
    logout_user,
)

from bookfinder import app
from bookfinder.models.bookfinderuser import BookfinderUser as User


@app.route('/profile')
@login_required
def profile():
    return render_template('profile/profile.html')


@app.route('/profile/delete_user')
def delete_user():
    u = User.get(id=current_user.id)
    logout_user()
    User.delete(u)
    flash('User {u} has been deleted'.format(u=u.username), 'success')
    return redirect('')
