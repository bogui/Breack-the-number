#! /usr/bin/env python

import requests
import re
import time
from sys import exit


"""Global variables and initial checks to guarantee the corect functionality"""
target = raw_input('Please enter a target: ')			#Ask the user for target.
#target = [http://YOUR TARGET HERE]				#If you prefere so, hardcode the target.
t = re.search('http://',target)
if not t:
	target = 'http://'+target
try:
	s = requests.get(target+'/number.php')			#Grab the session cookie.
except (requests.exceptions.ConnectionError,requests.exceptions.MissingSchema):
	sys.exit("Please define a target in format 'http://TARGET HERE' or\n'TARGET HERE' (without the 'http://' protocol part)!!!")		
cookie = dict(PHPSESSID=s.cookies['PHPSESSID'])			#Assign the cookie to a variable.
print "Extracting the session cookie"
time.sleep(5)
print "The cookie is - PHPSESSID="+s.cookies['PHPSESSID']
time.sleep(3)
print "Extracting numbers"
time.sleep(3)
#cookie = dict(PHPSESSID='barf62dadv7v46t991g9g8s2p5')		#Put your own cookie here! Or not?!?
extracting = 1							#Initiate the script.
the_num = ''							#Initiate the guessed number variable.
numbers = []							#Initiate the array of numbers.

"""Performs all general checks and dynamic variables assignments"""
def checks(income):
	out = re.findall('<p>(.+?)<br />The', income)
	getNum(out)
	val = re.findall('<br />The (.*?) number\?<br />', income)
	checkNum(val)
	end = re.findall('<center>(.*?)</center>',income)
	finish(end)

"""Gets the array of suplied numbers"""
def getNum(out):
	global numbers
	
	numbers = map(int, out[0].split(","))
	print numbers

"""Performs check of the suplied numbers depending of the rule"""
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
	print '\n'

"""Executes the post recuests to the remote server"""
def connection(payload, cookiee):
	p = requests.request('POST', target+'/proc.php', data = payload, cookies = cookiee)

"""If the flag is found stops the script and prints the flag"""
def finish(end):
	global extracting
	
	if end:
		extracting = 0
		print end[0]
		print '\n'

"""The Main loop"""	
def main():
	while extracting:
		r = requests.get(target+'/number.php', cookies = cookie)
		income = r.text
		checks(income)
		payload = {'number':the_num, 'submit':'submit'}
		connection(payload, cookie)
main()
