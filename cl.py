# EDIT THESE constants for your personal use
# Email parameters- make sure you use the proper login- you may need to use a dedicated "APP" password. CHECK your email provider!
# For instance you can find instructions for google mail here: https://support.google.com/accounts/answer/185833?hl=en
SMTP_SERVER = "smtp.fastmail.com"
SMTP_PORT = "587"
SMTP_LOGIN = "jko@fastmail.com"
SMTP_APP_PASSWORD = "jg44tvgn56qakhm7"

BLACKLIST_FILE = "/home/keith/blacklist.txt"

# point the CL_URL to your local CraigsList by changing 'Louisville' in the following example to your local city:
CL_URL = "https://louisville.craigslist.org/search/sss?query="

# areas are the craigslist areas nearby that I want to search. NOTE line is continued to two lines using backslash
# Play with CraigsList search "include nearby areas" using the drop-down menus to determine the areas you want to include
AREAS = "&sort=rel&searchNearby=2&nearbyArea=229&nearbyArea=342&nearbyArea=" \
    "35&nearbyArea=227&nearbyArea=45&nearbyArea=133&nearbyArea=673"

# You might also want to read the CraigsList help page on how to search: https://www.craigslist.org/about/help/search
######### BE CERTAIN to edit the above variables correctly!
#
# Nothing below this line needs editing for intended use ##############

import smtplib, sys
import requests, bs4

def mail_it(email_payload):
    import smtplib
    import datetime

    # now is the currrent time in my prefered format for an email subject
    now =datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p')

    connection_object = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    connection_object.ehlo()
    connection_object.starttls()
    connection_object.login(SMTP_LOGIN, SMTP_APP_PASSWORD)

    connection_object.sendmail(SMTP_LOGIN, SMTP_LOGIN, 'Subject: CraigsList notification at ' + now + '\n\n' + email_payload.decode('ascii','ignore'))
    connection_object.quit()
# end of mail_it function #############################################################################################

if len(sys.argv) > 1:
    # Get search keys from command line.
    search_keys = '+'.join(sys.argv[1:])
else:
    # alert for missing parameters then exit
    print("\nExiting... failed to find search keys/parameters!\n")
    exit()

request_object = requests.get(CL_URL + search_keys + AREAS)
request_object.raise_for_status()       # raise an exception for error codes (4xx or 5xx)
soup = bs4.BeautifulSoup(request_object.text, "lxml")

# blacklist.txt is storage for accumulated craigslist links already seen
blacklist_file = open(BLACKLIST_FILE, 'a+')    # open for appending and reading but will set pointer to EOF
blacklist_file.seek(0)  #set file pointer to beginning of file
blacklist = blacklist_file.readlines()  # create list of pid's contained in BLACKLIST_FILE
blacklist = [x.strip() for x in blacklist]  # strip out \n' and other whitespace characters
email = []      # initialize an empty list for use with accumulated/appended fields to go into the notification email

for i in range(len(soup.select('.rows li'))):
    pid = soup.select('.rows li')[i].get('data-pid')
    item = soup.select('.rows li')[i].p.a.text
    try:    # sometimes people don't put a price on their listings!
        price =soup.select('.rows li')[i].p.find('span', 'result-price').text
    except:
        price = "Price not found!"
    link = soup.select('.rows li')[i].p.a.get('href')

    if pid not in blacklist:    # don't want to see items already in the BLACKLIST_FILE
        print(item + "  " + price)
        print(pid + "\n")
        print(link)
        email.append(item + "  " + price)
        email.append(link)
        email.append(pid + "\n")
        blacklist_file.write(pid + "\n")    # Got these now so put in BLACKLIST_FILE


blacklist_file.close()

if len(email) > 0:              # If empty no notification needed
    email = '\n'.join(email)    # translate list into a string for email payload
    mail_it(email.encode('ascii','ignore'))  # send the notification as email by calling the mail_it function
