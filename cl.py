# EDIT THESE constants for your personal use
# Email parameters- make sure you use the proper login, and you may need to use a dedicated "APP" password. CHECK your email provider!
# For instance you can find instructions for google mail here: https://support.google.com/accounts/answer/185833?hl=en
SMTP_SERVER = "smtp.fastmail.com"
SMTP_PORT = "587"
SMTP_LOGIN = "jko@fastmail.com"
SMTP_APP_PASSWORD = "jg44tvgn56qakhm7"

SEARCHES_FILE = "/home/keith/cl_searches.txt"   # optionally create this file with one search per line
BLACKLIST_FILE = "/home/keith/cl_blacklist.txt" # file to accumulate the results from searches previously run

# point the CL_URL to your local CraigsList by changing 'Louisville' in the following example to your local city:
CITY = "Louisville" # CraigsList city, case insensitive

# areas are the craigslist 'nearby areas' that I want to search. NOTE this is continued to two lines using backslash
# Play with CraigsList search "include nearby areas" using the drop-down menus to determine the areas you want to include
AREAS = "&sort=rel&searchNearby=2&nearbyArea=229&nearbyArea=342&nearbyArea=" \
    "35&nearbyArea=227&nearbyArea=45&nearbyArea=133&nearbyArea=673"

# You might also want to read the CraigsList help page on how to search: https://www.craigslist.org/about/help/search
######### BE CERTAIN to edit the above variables correctly!
#
#####################    Nothing below this line needs editing for intended use    ##############

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

def soup_it():
    request_object = requests.get(cl_url + search_keys + AREAS) # get the CraigsList search results page
    request_object.raise_for_status()       # raise an exception for error codes (4xx or 5xx)
    soup = bs4.BeautifulSoup(request_object.text, "lxml")

    # BLACKLIST_FILE is storage for accumulated craigslist links already seen
    blacklist_file = open(BLACKLIST_FILE, 'a+')    # open for appending and reading but will set pointer to EOF
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
            print(item + "  " + price)  # these three print statements not necessary
            print(pid + "\n")
            print(link)
            email.append(item + "  " + price)
            email.append(link)
            email.append(pid + "\n")
            blacklist_file.write(pid + "\n")    # Got these now so put in BLACKLIST_FILE

    blacklist_file.close()
############# end of soup_it function ##########################################################################################

cl_url = "https://" + CITY + ".craigslist.org/search/sss?query="
email = []      # initialize an empty list for scraped results to go into the notification email

if len(sys.argv) > 1:
    # Get search keys from command line if present.
    search_keys = '+'.join(sys.argv[1:])
    searches = []
    searches.append(search_keys)    # searches list now contains only the one search reprented by the passed arguments on command line

else:
    try:    # if no command line parameters, look for SEARCHES_FILE which should have one search per line
        f = open(SEARCHES_FILE)
        searches = f.readlines()
        searches = [x.strip() for x in searches]
        searches = list(filter(None, searches))   # in case there's empty strings left over from a trailing \n in file or other
        f.close()
    except:
            # alert for missing parameters AND no SEARCHES_FILE found! then exit
            print("\nExiting... failed to find search keys/parameters! No args and no cl_searches.txt!\n")
            exit()

for search in searches: # the searches list now contains either the command line search/parameters or the searches from SEARCHES_FILE
    search_keys = search    # as we iterate thru the searches list
    soup_it()   # got the searches so now go get the CraigsList results, scrape, and append BLACKLIST_FILE for each search

if len(email) > 0:              # If empty no notification needed
    email = '\n'.join(email)    # translate list into a string for email payload
    mail_it(email.encode('ascii','ignore'))  # send the notification as email by calling the mail_it function
    # NOTE I'm encoding as ascii here then decoding to unicode inside the mail_it function to deal with stray junk that sometimes happens in CraigsList posts
