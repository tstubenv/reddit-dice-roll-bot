#!/usr/bin/python
import praw
import time
import re
import random
import traceback
import datetime
import sys

COMMENT_TEMPLATE = "Here are your dice rolls!"
BOT_DISCLAIMER = "^I'm ^a ^bot! ^PM ^me ^if ^something ^seems ^off."
results = []
values = []
user_agent = ("Random Dice Roll for r/rpg by /u/oldecrow")
r = praw.Reddit(user_agent=user_agent)
phrase = re.compile('\[r(\d*)d(\d*)([+*-/]?)(\d*?)(t?)(\d*?)\]')
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
#suggestion = re.compile('[sS]uggestion')
#roll = re.compile('[rR]oll')
#link = re.compile('[lL]ink')
#urladdress = re.compile('https?:\/\/www\.reddit\.com\/r\/rpg\/comments\/.*\/[^/]*\/.*')
sumlist = []
rollingsum=0
results = []
values = []
success = ''
successlist = []
dicetoroll, faces, mod, modnumber, threshtest, threshhold = ('','','','', False,'a')
limit = 500
print "logging in..."
########################################################################
r.login('DiceRollBot','REDACTED') ####REMOVE WHEN POSTING CODE#######
########################################################################
while True:
    print str(datetime.datetime.now()).split('.')[0]
    try:
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

        #for letter in r.get_inbox(limit=None):
        #   pass
        #subreddit = r.get_subreddit('bottest')
        subreddit = r.get_subreddit('rpg')
        for comment in subreddit.get_comments(limit=limit):
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
                    #print rolls
                    for q in range(len(rolls)):
                        dicetoroll, faces, mod, modnumber, threshtest,threshhold = rolls[q]
                        if threshtest == 't':
                            threshtest = True
                        elif threshtest != 't' and threshhold != '' and 'b':
                            modnumber = threshhold
                            threshhold = 'a'
                            threshtest = False
                        else:
                            threshtest = False
                        if int(rolls[q][0])<=20:
                            for i in range(int(rolls[q][0])):
                                print rolls[q]
                                number = random.randint(1,int(rolls[q][1]))
                                if mod == '+':
                                    number += int(modnumber)
                                elif mod == '*':
                                    number *= int(modnumber)
                                elif mod == '%':
                                    number = number/float(rolls[q][1])
                                    number = number * 100
                                    number = str(number)+'%'
                                elif mod == '-':
                                    number -= int(modnumber)
                                elif mod == '/':
                                        number /= int(modnumber)
                                #if threshhold != 'a' and threshhold != 'b':
                                if threshtest == True:
                                    if number >= int(threshhold):
                                        success = "roll succeeded!"
                                        threshhold = 'b'
                                        threshtest = False
                                    elif number < int(threshhold):
                                        success = "roll failed!"
                                elif threshhold == 'a':
                                    success = ''
                                elif threshhold == 'b':
                                    pass
                                results.append(number)
                            for n in range(len(results)):
                                rollingsum += int(results[n])
                            sumlist.append(rollingsum)
                            successlist.append(success)
                            values.append(results)
                            results = []
                            success = ''
                            threshhold = 'a'
                            rollingsum = 0
                            mod == None
                        else:
                            values.append('I can\'t do more than 20 dice at a time :\ ')
                            mod == None
                    if len(values) <= 15:
                        for p in range(len(values)):
                            try:
                                #print rolls[p][0]
                                if int(rolls[p][0]) > 1:
                                    if p == 0:
                                        #string = "for %sd%s:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
                                        string = "for %sd%s:  \n%s = %s  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'),sumlist[p], str(successlist[p]))
                                    else:
                                        #string = string+"  \n"+"for %sd%s:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
                                        string = string+"  \n"+"for %sd%s:  \n%s = %s  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'),sumlist[p], str(successlist[p]))
                                elif int(rolls[p][0]) == 1:
                                    if p == 0:
                                        #string = "for %sd%s:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
                                        string = "for %sd%s:  \n%s  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'), str(successlist[p]))
                                    else:
                                        #string = string+"  \n"+"for %sd%s:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
                                        string = string+"  \n"+"for %sd%s:  \n%s  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'), str(successlist[p]))
                            except:
                                break
                    else:
                        p = 0
                        while p <= 15:
                            try:
                                if int(rolls[p][0]) > 1:
                                    if p == 0:
                                        #string = "for %sd%s:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
                                        string = "for %sd%s:  \n%s = %s  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'),sumlist[p], str(successlist[p]))
                                    else:
                                        #string = string+"  \n"+"for %sd%s:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
                                        string = string+"  \n"+"for %sd%s:  \n%s = %s  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'),sumlist[p], str(successlist[p]))
                                elif int(rolls[p][0]) == 1:
                                    if p == 0:
                                        #string = "for %sd%s:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
                                        string = "for %sd%s:  \n%s  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'), str(successlist[p]))
                                    else:
                                        #string = string+"  \n"+"for %sd%s:  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'))
                                        string = string+"  \n"+"for %sd%s:  \n%s  \n%s" % (rolls[p][0],rolls[p][1],str(values[p]).strip('\[\]'), str(successlist[p]))
                                if p==15:
                                    string = string+"  \n"+"maximum of 15 roll commands per comment reached."
                                p+=1
                            except:
                                break
                    print "replying..."
                    comment.reply(COMMENT_TEMPLATE+"  \n"+string+"  \n"+BOT_DISCLAIMER)
                    sumlist = []
                    #print COMMENT_TEMPLATE+"  \n"+string+"  \n"+BOT_DISCLAIMER
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
                    print'done!'
                    results = []
                    success = ''
                    threshhold = 'a'
                    rollingsum = 0
                    mod == None
                    print "sleeping..."
                    limit = 20
                    time.sleep(120)
                    break
            time.sleep(1)
            mod = None
            limit = 20
            rollingsum = 0
    except KeyboardInterrupt:
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

LICENSE = """
Copyright (c) 2013, /u/oldecrow
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of the program nor /u/DiceRollBot nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRAN