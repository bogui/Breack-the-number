try:
	import requests
except(ImportError): 
	exit("\n[-]\tYou need Python Requests module in order for this script to work!\n")
from re import findall, search
from time import sleep
from sys import exit,stdout,version_info
from os import system

class ExtractNumsV3(object):

	extracting = 1							#Initiate the script.
	the_num = ''							#Initiate the guessed number variable.
	numbers = []							#Initiate the array of numbers.
	i = 1
	target = ''

	"""Wait function"""
	def wait(self, message):
		self.val = message
		for sec in range(1,7,1):
			for ch in ('/', '-', "\\", '|'):
				print(self.val, end='\t')
				sleep(0.1)				
				stdout.write(ch + "\r")	
		clr = ' ' * (len(message) + 6)
		stdout.write(clr + "\r")
		stdout.flush()
		return True		

	#wait(message='Initializing:')

	def target(self):
		global target
		"""Global variables and initial checks to guarantee the corect functionality"""
		target = input('[+]	Please enter a target in format "http://TARGET": ')			#Ask the user for target.
		#target = [http://YOUR TARGET HERE]				#If you prefere so, hardcode the target.
		# if not search('http://', target) or search('/(.+?).php',target):
		# 	exit('Please enter a target in format "http://TARGET"')
		t = search('http://',target)					#Simple check of the supplied input.
		if not t:
			target = 'http://'+target				#Securely add the target
		print("[+]\tTarget is:\t" + target)
		return target

	def cookie(self, target):
		try:
			s = requests.get(target+'/number.php')			#Grab the session cookie.
		except (requests.exceptions.ConnectionError,requests.exceptions.MissingSchema,NameError,ValueError):
			exit("\r\n[-]\tError!! Please check your target - %s - and try again!\n" % (target))
		#cookie = dict(PHPSESSID='barf62dadv7v46t991g9g8s2p5')		#Put your own cookie here! Or not?!?
		try:
			cookie = dict(PHPSESSID=s.cookies['PHPSESSID'])			#Assign the cookie to a variable.
		except(KeyError):
			exit("\n[-]\tThe supplied target do not provide any cookies!\n[-]\tPlease check and try again!")

		wait("\nExtracting the session cookie")

		print("\n\033[1;32m"+"The cookie is - PHPSESSID="+s.cookies['PHPSESSID']+"\033[0;32m")
		sleep(1)

		wait(self, "Extracting numbers")

		main(self)
	

	"""Performs all general checks and dynamic variables assignments"""
	def checks(self, income):
		out = findall('<p>(.+?)<br />The', income)
		getNum(out)
		val = findall('<br />The (.*?) number\?<br />', income)
		checkNum(val)
		end = findall('<center>(.*?)</center>',income)
		finish(end)

	"""Gets the array of suplied numbers"""
	def getNum(self, out):
		global numbers,i
		
		numbers = map(int, out[0].split(","))
		print("\n\nRequest No. "+'\033[38;5;45m'+str(i)+'\033[0;32m')
		i += 1
		print('\033[38;5;226m'+str(numbers)+'\033[0;32m')

	"""Performs check of the suplied numbers depending of the rule"""
	def checkNum(self, val):
		global the_num, extracting
		
		if str(val[0]) == 'maximum':
			the_num = max(numbers);
		elif str(val[0]) == 'minimum':
			the_num = min(numbers);
		else:
			print("Someting went wrong!")
			extracting = 0
		print('Guessing the '+'\033[38;5;214m'+val[0]+'\033[0;32m'+' number!')
		print('\033[38;5;226m'+str(the_num)+'\033[0;32m')

	"""Executes the post recuests to the remote server"""
	def connection(self, payload, cookiee):
		p = requests.request('POST', target+'/proc.php', data = payload, cookies = cookiee)

	"""If the flag is found stops the script and prints the flag"""
	def finish(self, end):
		global extracting
		
		if end:
			extracting = 0
			print("\033[1;32m"+"\n"+end[0])
			print('\n')

	"""The Main loop"""	
	def main(self):
		while extracting:
			r = requests.get(target+'/number.php', cookies = cookie)
			income = r.text
			checks(income)
			payload = {'number':the_num, 'submit':'submit'}
			connection(payload, cookie)