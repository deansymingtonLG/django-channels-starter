from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from channels.sessions import channel_session

@channel_session
def ws_connect(message):
  room = message.content['path'].strip("/")
  message.channel_session['room'] = room
  Group("chat-%s" % room).add(message.reply_channel)

@channel_session
def ws_message(message):
  Group("chat-%s" % message.channel_session['room']).send({
        "text": message['text'],
  })


# Connected to websocket.connect
def ws_add(message):
  Group("chat").add(message.reply_channel)

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
  Group("chat-%s").discard(message.reply_channel)
