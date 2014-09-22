from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ChannelForm(Form):
    channel_name = StringField('Channel name', validators=[DataRequired()])
    submit = SubmitField('Submit')
    descr = TextAreaField('Channel name')
