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
values  = []
user_agent = ("Random Dice Roll for r/rpg by /u/oldecrow")
r = praw.Reddit(user_agent=user_agent)
phrase = re.compile('\[r\d*d\d*[^0-9]{0,1}\d*\]')
test = re.compile('[^0-9]{1,}')
add = re.compile('\+')
sub = re.compile('\-')
div = re.compile('\/')
mult = re.compile('\*')
perc = re.compile('\%')
mod = None
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

########################################################################
r.login('DiceRollBot','REDACTED') ####REMOVE WHEN POSTING CODE#######
########################################################################

print "logging in..."
#subreddit = r.get_subreddit('bottest')
subreddit = r.get_subreddit('rpg')
comments = subreddit.get_comments()
for comment in subreddit.get_comments(limit=100):
	if controlNumber == 1:
		latestID = comment.id
	print "...fetching..."
	values = []
	if phrase.search(comment.body) and comment.id != comment_id:
		try:
			print "rolling..."
			print comment.id
			#print comment.body
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
							string = "for [r%sd%s]:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
						else:
							string = string+"  \n"+"for [r%sd%s]:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
					except:
						break
			else:
				p = 0
				while p <= 15:
					try:
						if p == 0:
							string = "for [r%sd%s]:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
						else:
							string = string+"  \n"+"for [r%sd%s]:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
						if p==15:
							string = string+"  \n"+"maximum of 15 roll commands per comment reached."
						p+=1
					except:
						break
			print "replying..."
			comment.reply(COMMENT_TEMPLATE+"  \n"+string+"  \n"+BOT_DISCLAIMER)
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