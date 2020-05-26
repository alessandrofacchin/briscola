from flask import Flask, render_template, redirect, url_for, request, flash
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask import request
from werkzeug.urls import url_parse
from flask_login import login_required
from app import db
from app.forms import RegistrationForm

from briscola.envs.game import Table


@app.route('/')
@app.route('/play')
@login_required
def play():
    tab = Table()
    last_play = {}
    tab.play_card(0)
    tab.play_card(0)
    tab.play_card(0)
    if tab.plays:
        last_play['winner'] = tab.plays[-1][0] == 1
        last_play['points'] = int(tab.plays[-1][1].points + tab.plays[-1][2].points)
        last_play['cards'] = tab.plays[-1][1:]
    else:
        last_play = None

    return render_template('play.html', middle_card=tab.middle_card, remaining_cards=len(tab.deck),
                           points=[int(tab.points[:, 0]), int(tab.points[:, 1])], hand_cards=tab.player_1,
                           played_card=tab.card_played, last_play=last_play)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('play'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('play')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('play'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('play'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
