"""
This is the settings file for use with:
craigslist_forsale_notify (cl.py), by Keith Ostertag 12/2017, GNU General Public License v3.0
https://github.com/keithostertag/craigslist_forsale_notify

SMTP parameters- make sure you use the proper login, and you may need to use a dedicated "APP" password.
Check your email provider for documentation.

For instance you can find instructions for google mail here: https://support.google.com/accounts/answer/185833?hl=en

The first four SMTP variables are NOT needed if you use the -l optional parameter for local mail only

If the first parameter you pass on the commandline is '-l' the script will use your local mail only
to send you notification of search results. Uses yourl system login as sender and recipient.

AREAS: the craigslist 'nearby areas' that you want to search.
Play with CraigsList search "include nearby areas" using the drop-down menus to determine the areas you want to include

CITY: CraigsList location you want to search

BLACKLIST_FILE: a plain text file to accumulate the results from searches previously run
the script will create this file at the path you give it- you must have read/write permisson to that path
"""

settings= {

    'SMTP_SERVER': "smtp.server.com",
    'SMTP_PORT': "587",
    'SMTP_LOGIN': "user@server.com",
    'SMTP_APP_PASSWORD': "xxxxxxxxxxxxxxxx",

    'SEARCHES_FILE': "/home/user/cl_searches.txt",   # optionally create this file with one search per line
    'BLACKLIST_FILE': "/home/user/cl_blacklist.txt", # file to accumulate the results from searches previously run

    'CITY': "Louisville", # CraigsList location, case insensitive


    # NOTE this is continued to two lines using the backslash
    'AREAS': "&sort=rel&searchNearby=2&nearbyArea=229&nearbyArea=342&nearbyArea=" \
        "35&nearbyArea=227&nearbyArea=45&nearbyArea=133&nearbyArea=673"
}
