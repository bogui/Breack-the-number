#! /usr/bin/env python

import requests
import re

"""Global variables"""
target = 'http://THE.TARGET/'				#Put your own target here! ;)
cookie = dict(PHPSESSID='barf62dadv7v46t991g9g8s2p5')	#Put your own cookie here! Or not?!?
extracting = 1						#Initiate the script.
the_num = ''
numbers = ''

"""Performs all general checks"""
def checks(input):
	out = re.findall(r'<p>(.+?)<br />The', input)
	getNum(out)
	val = re.findall(r'<br />The (.*?) number\?<br />', input)
	checkNum(val)
	end = re.findall('<center>(.*?)</center>',input)
	finish(end)

"""Gets the array of suplied numbers"""
def getNum(out):
	global numbers
	
	numbers = map(int, out[0].split(","))
	print numbers

"""Performs check of the suplied numbers"""
def checkNum(val):
	global the_num, extracting
	
	if str(val[0]) == 'maximum':
		the_num = max(numbers);
	elif str(val[0]) == 'minimum':
		the_num = min(numbers);
	else:
		print "Someting went wrong!";
		extracting = 0
	print 'Guessing the '+val[0]+' number!' 
	print the_num

"""Executes the post recuests to the remote server"""
def connection(payload, cookie):
	requests.request('POST', target+'proc.php', data = payload, cookies = cookie)

"""If the flag is found stops the script and prints the flag"""
def finish(end):
	global extracting
	
	if end:
		extracting = 0
		print end[0]

"""The Main loop"""	
while extracting:
	try:	
		r = requests.get(target+'number.php', cookies = cookie)
	except requests.exceptions.ConnectionError:
		print "The target is not defined!!! Please define target!!!"
		break
	input = r.text
	checks(input)
	payload = {'number':the_num, 'submit':'submit'}
	connection(payload, cookie)
