#!/usr/bin/python
import praw
import time
import re
import random
import traceback
import sys

COMMENT_TEMPLATE = "Here are your dice rolls!\n\n"
BOT_DISCLAIMER = "^I'm ^a ^bot! ^PM ^me ^if ^something ^seems ^off."
ROLL_TEMPLATE = "for %(command)s:  \n%(total)s (rolled %(rolls)s)\n\n"
INVALID_ROLL = "for %(command)s:  \nI'm sorry Dave, I'm afraid I can't do that.\n\n"
user_agent = ("Random Dice Roll for r/rpg by /u/oldecrow")
regex = re.compile(r"""
(?P<command>        # start command group
\[                  # '[' - opening bracket syntax
r                   # 'r' - rolling dice syntax
(?P<count>\d{1,2})  # 0-99 - number of dice
d                   # 'd' - rolling dice syntax
(?P<sides>\d{1,5})  # 0-99999 - number of sides
(                   # start optional modifier group
    (?P<operator>[\-+/*])   # '-', '+', '/', '*' - operator
    (?P<modifier>\d{1,5})   # 0-99999 - number to apply with operator
)?                  # end optional modifier group
\]                  # ']' - closing bracket syntax
)                   # end command group
""", re.VERBOSE)
# condensed form:
# r'(?P<command>\[r(?P<count>\d{1,2})d(?P<sides>\d{1,5})((?P<operator>[\-+/*])(?P<modifier>\d{1,5}))?\])'


def roll_dice(count, sides, operator=None, modifier=None, **kwargs):
    """Roll any number of dice with optional modifiers."""
    results = [] # keep track of each roll
    for die in count:
        results.append(random.randint(1, sides))
    total = sum(results)
    if modifier is None or operator is None:
        return (total, results)
    # apply modifier
    if operator == '+':
        total += modifier
    elif operator == '-':
        total -= modifier
    elif operator == '/':
        total /= modifier
    elif operator == '*':
        total *= modifier
    return (total, results)


def main():
    # try to load config
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
    
    r = praw.Reddit(user_agent=user_agent)
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
        
        if comment.id == comment_id:
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
            return # just in case sys.exit() didn't work...
        
        # build the comment string
        cumulative_roll_string = ''
        for roll_count, regex_match in enumerate(regex.finditer(comment.body)):
            try:
                # stop after 15 rolls
                if roll_count >= 15: # roll_count starts from 0
                    cumulative_roll_string += "Maximum of 15 roll commands per comment reached.\n\n"
                    break
                print "rolling..."
                print comment.id
                #print comment.body
                
                # parse command into a user-friendly dictionary
                command_dict = regex_match.groupdict()
                
                # do some pre-checking for invalid parameters
                if command_dict['sides'] == 0:
                    roll_string = INVALID_ROLL % command_dict
                elif command_dict['operator'] == '/' and command_dict['modifier'] == 0:
                    roll_string = INVALID_ROLL % command_dict
                else:
                    total, individual_rolls = roll_dice(**command_dict)
                
                    # fill roll string template with data
                    roll_string = ROLL_TEMPLATE % {
                        'command': command_dict['command'],
                        'total': total,
                        'rolls': ', '.join(individual_rolls)
                    }
                
                # add output string to other rolls
                cumulative_roll_string += roll_string
            except:
                print "ERROR!:\n"+comment.body
                traceback.print_exc(file=sys.stdout)
        print "replying..."
        comment.reply(COMMENT_TEMPLATE + cumulative_roll_string + BOT_DISCLAIMER)
        time.sleep(1)

if __name__ == '__main__':
    main()