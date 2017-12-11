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
request_object.raise_for_status()       # raise an exception for error codes (4xx or 5xx)
soup = bs4.BeautifulSoup(request_object.text, "lxml")

# blacklist.txt is storage for accumulated craigslist links that I have already seen
blacklist_file = open("/home/keith/blacklist.txt", 'a+')    # open for appending and reading but will set pointer to EOF
blacklist_file.seek(0)  #set file pointer to beginning of file
blacklist = blacklist_file.readlines()  # create list of pid's contained in blacklist_file
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

    if pid not in blacklist:    # don't want to see items already in the blacklist_file
        print(item + "  " + price)
        print(pid + "\n")
        print(link)
        email.append(item + "  " + price)
        email.append(link)
        email.append(pid + "\n")
        blacklist_file.write(pid + "\n")    # Got these now so put in blacklist_file


blacklist_file.close()

if len(email) > 0:              # anything in there? or is it empty?
    email = '\n'.join(email)    # translate list into a string for email payload
    mail_it(email)              # send the notificaiton as email by calling the mail_it function
