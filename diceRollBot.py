#!/usr/bin/python
import praw
import time
import re
import random
import traceback
import sys

COMMENT_TEMPLATE = "Here are your dice rolls!"
BOT_DISCLAIMER = "^I'm ^a ^bot! ^PM ^me ^if ^something ^seems ^off."
results = []
values = []
user_agent = ("Random Dice Roll for r/rpg by /u/oldecrow")
r = praw.Reddit(user_agent=user_agent)
phrase = re.compile('\[r\d*d\d*[^0-9]{0,1}\d*\]')
#phrase = re.compile(r"""
#(?P<command>        # start command group
#\[                  # '[' - opening bracket syntax
#r                   # 'r' - rolling dice syntax
#(?P<count>\d{1,2})  # 0-99 - number of dice
#d                   # 'd' - rolling dice syntax
#(?P<sides>\d{1,5})  # 0-99999 - number of sides
#(                   # start optional modifier group
#   (?P<operator>[\-+/*])   # '-', '+', '/', '*' - operator
#   (?P<modifier>\d{1,5})   # 0-99999 - number to apply with operator
#)?                  # end optional modifier group
#\]                  # ']' - closing bracket syntax
#)                   # end command group
#""", re.VERBOSE) # this amazingly awesome regex brought to you by /u/Durinthal
test = re.compile('[^0-9]{1,}')
add = re.compile('\+')
sub = re.compile('\-')
div = re.compile('\/')
mult = re.compile('\*')
perc = re.compile('\%')
suggestion = re.compile('[sS]uggestion')
roll = re.compile('[rR]oll')
link = re.compile('[lL]ink')
urladdress = re.compile('https?:\/\/www\.reddit\.com\/r\/rpg\/comments\/.*\/[^/]*\/.*')
sumlist = []
mod = None

print "logging in..."
########################################################################
r.login('DiceRollBot','REDACTED') ####REMOVE WHEN POSTING CODE#######
########################################################################

f = open('LatestDone.conf','r')
try: 
	comment_id = f.read()
	comment_id = comment_id.rstrip()
	controlNumber = 1
except:
	traceback.print_exc(file=sys.stdout)
	f.close()
	sys.exit("Couldn't read file")
finally:
	f.close()

for letter in r.get_inbox(limit=None):
	pass
#subreddit = r.get_subreddit('bottest')
subreddit = r.get_subreddit('rpg')
comments = subreddit.get_comments()
for comment in subreddit.get_comments(limit=None):
	if controlNumber == 1:
		latestID = comment.id
		controlNumber+=1763432
	print "...fetching..."
	print 'latest :'+latestID
	print 'old    :'+comment_id
	print 'current:'+comment.id
	values = []
	if phrase.search(comment.body) and comment.id != comment_id:
		try:
			print "rolling..."
			rolls = phrase.findall(comment.body)
			for q in range(len(rolls)):
				rolls[q] = rolls[q].strip('\[r\]')
				rolls[q] = rolls[q].split('d')
				if test.search(rolls[q][1]) != None:
					if add.search(rolls[q][1]) != None:
						temp = [rolls[q][0]]
						rolls[q]= temp+rolls[q][1].split('+')
						mod = '+'
					elif mult.search(rolls[q][1]) != None:
						temp = [rolls[q][0]]
						rolls[q]= temp+rolls[q][1].split('*')
						mod = '*'
					elif perc.search(rolls[q][1]) != None:
						temp = [rolls[q][0]]
						rolls[q]= temp+rolls[q][1].split('%')
						mod = '%'
					elif sub.search(rolls[q][1]) != None:
						temp = [rolls[q][0]]
						rolls[q]= temp+rolls[q][1].split('-')
						mod = '-'
					elif div.search(rolls[q][1]) != None:
						temp = [rolls[q][0]]
						rolls[q]= temp+rolls[q][1].split('/')
						mod = '/'
				if int(rolls[q][0])<=20:
					for i in range(int(rolls[q][0])):
						number = random.randint(1,int(rolls[q][1]))
						if mod != None:
							if mod == '+':
								number += int(rolls[q][2])
							elif mod == '*':
								number *= int(rolls[q][2])
							elif mod == '%':
								number = number/float(rolls[q][1])
								number = number * 100
								number = str(number)+'%'
							elif mod == '-':
								number -= int(rolls[q][2])
							elif mod == '/':
								number /= int(rolls[q][2])
						results.append(number)
					for n in range(len(results)):
						rollingsum += int(results[n])
					sumlist.append(rollingsum)
					values.append(results)
					results = []
					mod == None
				else:
					values.append('I can\'t do more than 20 dice at a time :\ ')
					mod == None
			if len(values) <= 15:
				for p in range(len(values)):
					try:
						if p == 0:
							string = "for %sd%s:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
							#string = "for %sd%s:  \n%s = %s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'),sumlist[p])
						else:
							string = string+"  \n"+"for %sd%s:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
							#string = string+"  \n"+"for %sd%s:  \n%s = %s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'), sumlist[p])
					except:
						break
			else:
				p = 0
				while p <= 15:
					try:
						if p == 0:
							string = "for %sd%s:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
							#string = "for %sd%s:  \n%s = %s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'), sumlist[p])
						else:
							string = string+"  \n"+"for %sd%s:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
							#string = string+"  \n"+"for %sd%s:  \n%s = %s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'), sumlist[p])
						if p==15:
							string = string+"  \n"+"maximum of 15 roll commands per comment reached."
						p+=1
					except:
						break
			print "replying..."
			comment.reply(COMMENT_TEMPLATE+"  \n"+string+"  \n"+BOT_DISCLAIMER)
			print COMMENT_TEMPLATE+"  \n"+string+"  \n"+BOT_DISCLAIMER
		except:
			print "ERROR!:\n"+comment.body
			traceback.print_exc(file=sys.stdout)
	#else:
		#print "nothing"
	elif comment.id == comment_id:
		f = open('LatestDone.conf', 'w')
		try:
			f.write(latestID)
			print "configuring..."
			controlNumber += 42
		except:
			traceback.print_exc(file=sys.stdout)
			f.close()
			sys.exit("Couldn't write file")
		finally:
			f.close()
			sys.exit('done!')
	time.sleep(1)
	mod = None
	rollingsum = 0
	
LICENSE = """
Copyright (c) 2013, /u/oldecrow
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of the program nor /u/DiceRollBot nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""