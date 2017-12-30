"""
craigslist_forsale_notify (cl.py), by Keith Ostertag 12/2017, GNU General Public License v3.0
https://github.com/keithostertag/craigslist_forsale_notify

craigslist_forsale_notify is a small python3 script (running under Linux from the command line)
which aims to replace the Craigs List email notification functionality of 'saved searches' for
personal use of the "For Sale" category. This script is designed for and tested on Linux OS only.

You must manually edit the variables in the cl_settings.py file to use this script.

You might also want to read the CraigsList help page on how to search: https://www.craigslist.org/about/help/search

See the README.md file for more details and examples.
"""

#####################    Nothing below this line needs editing for intended use    ##############

import smtplib, sys, os
import requests, bs4
import datetime
from cl_settings import settings

def mail_it(email_payload):

    connection_object = smtplib.SMTP(settings['SMTP_SERVER'], settings['SMTP_PORT'])
    connection_object.ehlo()
    connection_object.starttls()
    connection_object.login(settings['SMTP_LOGIN'], settings['SMTP_APP_PASSWORD'])

    connection_object.sendmail(settings['SMTP_LOGIN'], settings['SMTP_LOGIN'], 'Subject: CraigsList notification at ' + now + '\n\n' + email_payload.decode('ascii','ignore'))
    connection_object.quit()

# end of mail_it function #############################################################################################

def soup_it():
    request_object = requests.get(cl_url + search_keys + settings['AREAS']) # get the CraigsList search results page
    request_object.raise_for_status()       # raise an exception for error codes (4xx or 5xx)
    soup = bs4.BeautifulSoup(request_object.text, "lxml")

    # BLACKLIST_FILE is storage for accumulated craigslist links already seen
    blacklist_file = open(settings['BLACKLIST_FILE'], 'a+')
    blacklist_file.seek(0)  #set file pointer to beginning of file
    blacklist = blacklist_file.readlines()  # create list of pid's contained in BLACKLIST_FILE
    blacklist = [x.strip() for x in blacklist]  # strip out \n' and other whitespace characters

    for i in range(len(soup.select('.rows li'))):
        pid = soup.select('.rows li')[i].get('data-pid')    # data-pid is the key CraigsList uses to uniquely identify posts
        item = soup.select('.rows li')[i].p.a.text
        try:    # sometimes people don't put a price on their listings!
            price =soup.select('.rows li')[i].p.find('span', 'result-price').text
        except:
            price = "Price not found!"
        link = soup.select('.rows li')[i].p.a.get('href')

        if pid not in blacklist:    # don't want to see items already in the BLACKLIST_FILE
            # print(item + "  " + price)  # these three print statements not necessary but can be handy
            # print(pid + "\n")
            # print(link)
            email.append(item + "  " + price)
            email.append(link)
            email.append(pid + "\n")
            blacklist_file.write(pid + "\n")    # Got these now, so put in BLACKLIST_FILE

    blacklist_file.close()

############# end of soup_it function ####################################################################

def local_mail_only(email):

    from email.message import EmailMessage

    msg = EmailMessage()
    msg.set_content(email)
    msg['Subject'] = "Craig's List notification at " + now
    msg['From'] = os.getlogin() + "@localhost"
    msg['To'] = os.getlogin() + "@localhost"
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit

############ end of local_mail_only function  ##########################################################

cl_url = "https://" + settings['CITY'] + ".craigslist.org/search/sss?query="
now =datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p')
email = []      # initialize an empty list for scraped results to go into the notification email

if len(sys.argv) > 1:
    # Get search keys from command line if present. Check if optional parameter -l is first
    search_keys = '+'.join(sys.argv[2:]) if sys.argv[1] == '-l' else '+'.join(sys.argv[1:])
    searches = []
    searches.append(search_keys)    # searches list now contains only the one search represented by the passed arguments on command line

else:
    try:    # if no command line parameters, look for SEARCHES_FILE (which should have one search per line)
        f = open(settings['SEARCHES_FILE'])
        searches = f.readlines()
        f.close()
        searches = [x.strip() for x in searches if x != None]
    except:
            # alert for missing parameters AND no SEARCHES_FILE found! then exit
            print("\nExiting... failed to find search keys/parameters! No args and no cl_searches.txt!\n")
            exit()

for search in searches: # the searches list now contains either the command line search/parameters or the searches from SEARCHES_FILE
    search_keys = search    # as we iterate thru the searches list
    soup_it()   # got the searches so now go get the CraigsList results, scrape, and append BLACKLIST_FILE for each search

if len(email) > 0:              # If empty no notification needed
    email = '\n'.join(email)    # translate list into a string for email payload

# send the notification as email by calling the mail_it function
# OR if -l argument is passed just use local_mail_only function
# NOTE I'm encoding as ascii here then decoding to unicode inside the mail_it function to deal with stray junk that sometimes happens in CraigsList posts

    if len(sys.argv) >= 2 and sys.argv[1] == '-l':
        local_mail_only(email)
    else:
        mail_it(email.encode('ascii','ignore'))
