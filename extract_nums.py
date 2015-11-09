#! /usr/bin/env python

import requests
from re import findall, search
from time import sleep
from sys import exit,stdout
from os import system

"""Global variables and initial checks to guarantee the corect functionality"""
target = raw_input('Please enter a target: ')			#Ask the user for target.
#target = [http://YOUR TARGET HERE]				#If you prefere so, hardcode the target.
t = search('http://',target)			#Simple check of the supplied input.
if not t:
	target = 'http://'+target
try:
	s = requests.get(target+'/number.php')			#Grab the session cookie.
except (requests.exceptions.ConnectionError,requests.exceptions.MissingSchema,NameError):
	exit("Please define a target in format 'http://TARGET HERE' or\n'TARGET HERE' (without the 'http://' protocol part)!!!")		
try:
	cookie = dict(PHPSESSID=s.cookies['PHPSESSID'])			#Assign the cookie to a variable.
except(KeyError):
	exit("\nThe supplied target do not provide any cookies!\nPlease check the target and try again!")
print "\nExtracting the session cookie",
for sec in range(1,7,1):
	stdout.flush()
	sleep(0.7)
	print '.',
print "\nThe cookie is - PHPSESSID="+s.cookies['PHPSESSID']
sleep(1)
print "Extracting numbers",
for sec in range(1,7,1):
	sleep(0.7)
	stdout.flush()
	print '.',
#cookie = dict(PHPSESSID='barf62dadv7v46t991g9g8s2p5')		#Put your own cookie here! Or not?!?
extracting = 1							#Initiate the script.
the_num = ''							#Initiate the guessed number variable.
numbers = []							#Initiate the array of numbers.
i = 1

"""Performs all general checks and dynamic variables assignments"""
def checks(income):
	out = findall('<p>(.+?)<br />The', income)
	getNum(out)
	val = findall('<br />The (.*?) number\?<br />', income)
	checkNum(val)
	end = findall('<center>(.*?)</center>',income)
	finish(end)

"""Gets the array of suplied numbers"""
def getNum(out):
	global numbers,i
	
	numbers = map(int, out[0].split(","))
	print "\n\nRequest No. "+str(i)
	i = i + 1
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
		stdout.flush()
		r = requests.get(target+'/number.php', cookies = cookie)
		income = r.text
		checks(income)
		payload = {'number':the_num, 'submit':'submit'}
		connection(payload, cookie)
main()