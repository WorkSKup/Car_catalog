import os
from flask import render_template, redirect, url_for, flash
from sqlalchemy import select
from flask_login import logout_user, current_user, login_required, login_user
from werkzeug.utils import secure_filename
from .models import User, Car
from .forms import RegistrationForm, LoginForm
from app import app, db

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return 'You already authenticated'

    form = RegistrationForm()
    if form.validate_on_submit():
        with db.session() as session:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            uploaded_file = form.photo.data
            filename = secure_filename(uploaded_file.filename)
            avatar_path = os.path.join(app.config['UPLOAD_PATH'], filename)
            uploaded_file.save(avatar_path)
            relative_path = os.path.join('uploads', filename).replace('\\', '/')
            user.photo = relative_path
            session.add(user)
            session.commit()
        flash('You complete registration', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return 'You already authenticated'

    form = LoginForm()
    if form.validate_on_submit():
        with db.session() as session:
            user = session.scalar(
                select(User).where(User.email == form.email.data)
            )
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))