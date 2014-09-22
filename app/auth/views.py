from flask import render_template, flash, redirect, url_for, g
from .forms import LoginForm, RegisterForm
from . import auth
from flask.ext.login import login_user, login_required, logout_user, current_user
from ..models import User
from .. import db


@auth.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return redirect('/channels')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.nickname.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)
            return redirect('/channels')
        flash('Incorrect password')
    return render_template('login.html', form=LoginForm())

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data, username=form.nickname.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('registration.html', form=RegisterForm())


