# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import time
from threading import Thread
from flask import render_template, session, request, redirect
from app import socketio
from flask.ext.socketio import emit, join_room, leave_room
from . import chat
from flask.ext.login import current_user, login_required
from ..models import Channel, User
from .forms import ChannelForm
from app import db

thread = None


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(120)
        count += 1
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count, 'nickname': 'Server'},
                      namespace='/chat')

@login_required
@chat.route('/chat/<chatname>')
def index(chatname):
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()
    users = Channel.query.filter_by(name=chatname).first().users
    current_user.channel_id = Channel.query.filter_by(name=chatname).first().id
    return render_template('chat.html', chat=chatname, username=current_user.username, users=users)


@login_required
@chat.route('/channels', methods=['GET', 'POST'])
def channels():
    channels_list = Channel.query.all()
    form = ChannelForm()
    if form.validate_on_submit():
        channel = Channel(name=form.channel_name.data, descr=form.descr.data)
        db.session.add(channel)
        db.session.commit()
        return redirect('/channels')
    return render_template('channels.html', channels=channels_list, form=ChannelForm())

@socketio.on('my event', namespace='/chat')
def test_message(message):

    emit('my response',
         {'data': message['data'], 'nickname': current_user.username})



@socketio.on('join', namespace='/chat')
def join(message):
    join_room(message['room'])



@socketio.on('leave', namespace='/chat')
def leave(message):
    leave_room(message['room'])



@socketio.on('send msg', namespace='/chat')
def send_room_message(message):
    emit('my response',
         {'data': message['data'], 'nickname': current_user.username},
         room=message['room'])


@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected')

@socketio.on('leaving channel', namespace='/chat')
def leaving(message):
    User.query.filter_by(username=message['username']).first().channel_id = None
    emit('leaver', {'data': message['username']}, broadcast=True)

@socketio.on('new user', namespace='/chat')
def new_user(message):
    emit('refresh users', {'data': message['username']}, room=message['roomname'])


