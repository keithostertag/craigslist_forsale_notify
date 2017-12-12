**craigslist_notify** is a small python 3 script (running under Linux on the command line) which aims to replace the Craigs List email notification functionality of 'saved searches' for personal use of the "For Sale" category. This script is designed for and tested on Linux OS only, but can likely be easily modified for other OS's. Support for English only.

#### Overview of how it works:
1. You must setup the requirements on your system.
2. You must edit the script to include the city and nearby areas you want to search, plus your correct SMTP server and email information.
3. Run the script (from the command line or for use with Crontab) with your search terms as command line arguments (separated by spaces).
4. The script uses Requests to download the search results page then uses BeautifulSoup to scrape for the pid, item, price, and url of the results.
5. The script then uses SMTP to send the results to your provided email address.
6. The script also creates/appends a file which keeps track of the pid's so it won't send you them a second time.

#### Benefits:
1. Run it when and as many times as you like.  The CraigsList 'Saved searches' function has an odd algorithm for when it runs, and you have no control.
2. Won't repeat results as it keeps track of which items you have already seen.  The CraigsList 'Saved searches' function will keep sending you the same items.


#### Requirements:
1. Of course you need an email address and the correct SMTP info to access it.
2. Python 3 running on Linux.
3. These Python modules properly installed (generally with pip): request, BeautifulSoup, lxml.
4. A path to where the script can write to a file.
