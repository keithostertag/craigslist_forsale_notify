import smtplib, sys
import requests, bs4

def mail_it(email_payload):
    import smtplib
    import datetime

    # now is the currrent time in my prefered format for an email subject
    now =datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p')

    connection_object = smtplib.SMTP('smtp.fastmail.com', 587)
    connection_object.ehlo()
    connection_object.starttls()
    connection_object.login('jko@fastmail.com', 'jg44tvgn56qakhm7')
    connection_object.sendmail('jko@fastmail.com', 'jko@fastmail.com', 'Subject: CraigsList notification at ' + now + '\n\n' + email_payload)
    connection_object.quit()
# end of mail_it function #############################################################################################

if len(sys.argv) > 1:
    # Get search keys from command line.
    search_keys = '+'.join(sys.argv[1:])
else:
    # alert for missing parameters then exit
    print("\nExiting... failed to find search keys/parameters!\n")
    exit()

# areas are the craigslist areas nearby that I want to search. NOTE line is continued to two lines using backslash
areas = "&sort=rel&searchNearby=2&nearbyArea=229&nearbyArea=342&nearbyArea=" \
    "35&nearbyArea=227&nearbyArea=45&nearbyArea=133&nearbyArea=673"

request_object = requests.get('https://louisville.craigslist.org/search/sss?query=' + search_keys + areas)
request_object.raise_for_status()
soup = bs4.BeautifulSoup(request_object.text, "lxml")

# blacklist.txt is storage for accumulated craigslist links that I have already seen
blacklist_file = open("/home/keith/blacklist.txt", 'a+')    # open for appending and reading but will set pointer to EOF
blacklist_file.seek(0)  #set file pointer to beginning of file
blacklist = blacklist_file.readlines()  # create list of pid's contained in blacklist_file
blacklist = [x.strip() for x in blacklist]  # strip out \n's
email = []

try:
    for i in range(len(soup.select('.rows li'))):
        if soup.select('.rows li')[i].get('data-pid') not in blacklist: # don't want to see the pids in the blacklist
            print(soup.select('.rows li')[i].p.a.text + "  " + soup.select('.rows li')[i].p.find('span', 'result-price').text)
            print(soup.select('.rows li')[i].p.a.get('href'))       #link
            print(soup.select('.rows li')[i].get('data-pid') + "\n")
            email.append(soup.select('.rows li')[i].p.a.text + "  " + soup.select('.rows li')[i].p.find('span', 'result-price').text)
            email.append(soup.select('.rows li')[i].p.a.get('href'))       #link
            email.append(soup.select('.rows li')[i].get('data-pid') + "\n")
            blacklist_file.write(soup.select('.rows li')[i].get('data-pid') + "\n") # got these now so put them in blacklist
        continue
except:
    blacklist_file.close()
    # exit()

blacklist_file.close()

if len(email) > 0:              # anything in there? or is it empty?
    email = '\n'.join(email)    # translate list into a string for email payload
    mail_it(email)              # send the notificaiton as email by calling the mail_it function
