import requests
import re
import random
from bs4 import BeautifulSoup
from collections import defaultdict
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)
line_bot_api = LineBotApi("v1GlFwS8CKO4fcVxBkgvrgmqV0pOyfjlddk0QnXmJ4Li4h/U9MQtC+YjaxgEkVteMKWCsewSveyySzvnqpyAJ6hnvZ6zyO6uicKl/5LGi7aZG+4d/LIzGpq0IqoyIU4r3gCYB7kQnmEoRhPK2I/zgQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("d31decc7af67c2b7cc4aef2863646739")
help = ["指令","help"]
state = "normal"
@app.route('/')
def index():
  return 'hello my line bot'

def printlog(event):
	print("event.reply_token:", event.reply_token)
	print("event.type:", event.type)
	print("event.timestamp:", event.timestamp)
	print("event.source.type",event.source.type)
	if event.source.type is "user":
		profile = line_bot_api.get_profile(event.source.user_id)
		print("event.source.user_id",event.source.user_id)
		print(profile.display_name)
		print(profile.user_id)
		print(profile.picture_url)
		print(profile.status_message)
	elif event.source.type is "room":
		print("event.source.room_id",event.source.room_id)
	elif event.source.type is "group":
		print("event.source.group_id",event.source.group_id)
	print("event.message.id",event.message.id)
	if event.message.type is "text":
		print("event.source.type",event.message.text)
	elif event.message.type is "sticker":
		print("event.source.package_id",event.message.package_id)
		print("event.source.sticker_id",event.message.sticker_id)	
	return 0

@app.route("/callback", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']
	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)
	return 'OK'

@handler.add(JoinEvent)
def handle_join(event):
	msg = 'Joined this {}!\nみなさん、よろしくお願いします :)'.format(event.source.type)
	line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.source.type))
	return 0

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	printlog(event)
	if event.message.text in help :
		#state = "normal"
		buttons_template = TemplateSendMessage(alt_text='Buttons template',
			template=ButtonsTemplate(title='選擇服務',text='請選擇',thumbnail_image_url='https://i.imgur.com/jz3tOwL.jpg',
			actions=[MessageTemplateAction(label='echo',text='echo')
				#URITemplateAction(label='',uri=''),
				#URITemplateAction(label='',uri=''),
				#URITemplateAction(label='',uri='')
				]))
		line_bot_api.reply_message(event.reply_token, buttons_template)
		return 0
	else:
		#state = "echo"
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
		return 0

@handler.add(MessageEvent, message=StickerMessage)
def handle_message(event):
	printlog(event)
	return 0

@handler.add(MessageEvent, message=AudioMessage)
def handle_message(event):
	printlog(event)
	return 0

@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
	printlog(event)
	return 0

@handler.add(MessageEvent, message=VideoMessage)
def handle_message(event):
	printlog(event)
	return 0

if __name__ == "__main__":
	app.run()