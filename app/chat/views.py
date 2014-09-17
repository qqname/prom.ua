# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import time
from threading import Thread
from flask import render_template, session, request
from app import socketio
from flask.ext.socketio import emit, join_room, leave_room
from . import chat
from flask.ext.login import current_user

thread = None


def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        time.sleep(5)
        emit('my response',
             {'data': 'Server generated event', 'nickname': 'Server'},
            namespace='/chat',
            broadcast=True)


@chat.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()
    return render_template('chat.html')



@socketio.on('my event', namespace='/chat')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'nickname': message['nickname'] or current_user.username})


@socketio.on('my broadcast event', namespace='')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']})


@socketio.on('leave', namespace='')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']})


@socketio.on('my room event', namespace='')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('connect', namespace='chat')
def test_connect():
    socketio.emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='')
def test_disconnect():
    print('Client disconnected')


