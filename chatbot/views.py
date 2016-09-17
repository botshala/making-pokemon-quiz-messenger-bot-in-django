#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests
import re

# Create your views here.

VERIFY_TOKEN = '7thseptember2016'
PAGE_ACCESS_TOKEN = 'EAAZAyhaPaTVoBALdXcRNojTqUTCZBdpNxHicITYZBFfw8jtqyMwGRGf2bEO9EqF9P2umFknFXKpbBoZAFwx3myMUDnZC6RnC5xeR3qFGOFTxTs2tP1OyIZAxeyyddoWlSj5qSLcpCunfPZA0drzhlAp8HlMIpMFKos9MbAaB9iDjQZDZD'


def index(request):
	post_facebook_message('1406994739523556','hi')
	handle_postback('1406994739523556','hi')
	#t = request.GET['text'] or 'foo'
	output_text = chuck()
	return HttpResponse(output_text)

def chuck():
	url = 'https://api.chucknorris.io/jokes/random'
	resp = requests.get(url=url).text
	data = json.loads(resp)
	return data['value'], data['url']


def wikisearch(title='tomato'):
    url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=%s'%(title)
    resp = requests.get(url=url).text
    data = json.loads(resp)

    scoped_data = data['query']['pages']
    page_id = data['query']['pages'].keys()[0]
    wiki_url = 'https://en.m.wikipedia.org/?curid=%s'%(page_id)
    try:
        wiki_content = scoped_data[page_id]['extract']
        wiki_content = re.sub(r'[^\x00-\x7F]+',' ', wiki_content)
        wiki_content = re.sub(r'\([^)]*\)', '', wiki_content)
        
        if len(wiki_content) > 315:
            wiki_content = wiki_content[:315] + ' ...'
    except KeyError:
        wiki_content = ''

    return wiki_content


def post_facebook_message(fbid,message_text):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	
	#output_text = wikisearch(message_text)
	output_text,output_url = chuck()
	output_text = output_text.replace("Chuck Norris", "Rajnikanth")

	response_msg_with_button = {

				"recipient":{
				    "id":fbid
				  },

				  "message":{
				    "attachment":{
				      "type":"template",
				      "payload":{
				        "template_type":"button",
				        "text":output_text,
				        "buttons":[
				          {
				            "type":"web_url",
				            "url":output_url,
				            "title":"Show Website"
				          },
				          {
				            "type":"postback",
				            "title":"Start Chatting",
				            "payload":"USER_DEFINED_PAYLOAD"
				          }
				        ]
				      }
				    }
				  }

	}

	response_msg_with_button = json.dumps(response_msg_with_button)

	#response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":output_text}})
	#status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	
	status = requests.post(post_message_url, 
			headers={"Content-Type": "application/json"},
			data=response_msg_with_button)
	
	print status.json()

def handle_postback(fbid,payload):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	output_text = 'Payload Recieved: ' + payload

	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":output_text}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
		

class MyChatBotView(generic.View):
	def get (self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Oops invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		incoming_message= json.loads(self.request.body.decode('utf-8'))
		print incoming_message

		for entry in incoming_message['entry']:
			for message in entry['messaging']:

				try:
					if 'postback' in message:
						handle_postback(message['sender']['id'],message['postback']['payload'])
					else:
						pass
				except Exception as e:
					print e
				
				try:
					sender_id = message['sender']['id']
					message_text = message['message']['text']
					post_facebook_message(sender_id,message_text) 
				except Exception as e:
					print e

		return HttpResponse()  


