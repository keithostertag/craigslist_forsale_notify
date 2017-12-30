**craigslist_forsale_notify** is a small python3 script (running under Linux from the command line) which aims to replace the Craigs List email notification functionality of 'saved searches' for personal use of the "For Sale" category. This script is designed for and tested on Linux OS only, but can likely be easily modified for other OS's. Support for English only. Probably wouldn't be difficult to modify to search other categories, but I leave that to you. Can also easily be edited to access other CL sections, like Apartments!

Since CraigsList does not provide a public API, this script uses scraping to capture information. This script will need to be modified if CraigsList changes their page/data structure.

#### Overview of how it works:
1. You setup the requirements on your system.
2. You edit the cl_settings file to include the location and nearby areas you want to search, plus your correct SMTP server and email information.
3. You run the script (from the command line or with Crontab) with your search terms as command line arguments (separated by spaces).
4. The script uses Requests to download the search results page then uses BeautifulSoup to scrape for the pid, item, price, and url of the results.
5. The script then uses SMTP to send the results to your provided email address.
6. The script also creates/appends a BLACKLIST_FILE which keeps track of the pid's so it won't send you them a second time on future searches.
7. Optionally- if you set the first commandline parameter to "-l" the script will only email your local user account (on your machine or potentially on your local private network).

#### Benefits:
1. Run it when and as many times as you like.  By contrast, the CraigsList 'Saved searches' function has an odd algorithm for when it runs, and you have no control.
2. Won't repeat results as it keeps track of which items you have already seen.  By contrast, the CraigsList 'Saved searches' function will keep sending you the same items.
3. Optionally- with the "-l" parameter you can receive search results when you don't or can't use your regular Internet email (uses your local system login as sender and recipient).


#### Requirements:
1. An email address and the correct SMTP info to access it, unless using the -l optional parameter
2. Python3 running on Linux.
3. These Python modules properly installed (generally with pip):  
  * requests
  * BeautifulSoup4
  * lxml

4. A path to where the script can write the BLACKLIST_FILE file.

#### Examples of how I use this script:
There are a few items which appear on CraigsList infrequently that I like to follow over the course of several months. Here is an example of the content of my SEARCHES_FILE which I keep in my home directory:

```  
keith@ada:~$ cat cl_searches.txt
(tektronix | agilent | hp) (oscilloscope* | scope*) -buy
"hemp oil" | "hemp soap"
minolta autocord
hasselblad
"bay 1 filter"
```  
If I wanted to add a search to my SEARCHES_FILE for, say, concert tickets, I could just do this at the command line:

```
keith@ada:~$ echo \"pink floyd\" \"concert tickets\">> cl_searches.txt
```  

Or just run it manually from the command line whenever:
```  
keith@ada:~/code/cl$ python3 cl.py "pink floyd" "concert tickets"
```  

Though typically I just let in run from the crontab once a day (or even hourly sometimes).

When I don't want to run an email client or for some reason don't want the results sent to my regular Internet email I just use the  optional "-l" parameter on the commandline and use my system mail, as follows:

```
keith@ada:~$ python3 cl.py -l "dell latitude i7"
keith@ada:~$
keith@ada:~$ mail
Mail version 8.1.2 01/15/2001.  Type ? for help.
"/var/mail/keith": 1 message 1 new
>N  1 keith@localhost    Fri Dec 15 18:11   46/1611  Craig's List notificatio
& 1
Message 1:
From keith@localhost Fri Dec 15 18:11:51 2017
Envelope-to: keith@localhost
Delivery-date: Fri, 15 Dec 2017 18:11:51 -0500
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 7bit
MIME-Version: 1.0
Subject: Craig's List notification at 2017-12-15 06:11 PM
From: keith@localhost
To: keith@localhost
Date: Fri, 15 Dec 2017 18:11:51 -0500

Dell Latitude E7440 UltraBook Core i7-16GB-256GB SSD Windows 10 Pro  $225
https://cincinnati.craigslist.org/ele/d/dell-latitude-e7440-ultrabook/6421223747.html
6421223747

Laptop Dell latitude E7440, Intel i7, 16gb RAM , 256GB SSD storage.  $360
https://louisville.craigslist.org/sys/d/laptop-dell-latitude-e7440/6418370643.html
6418370643

Dell latitude e6430 i7 16 gb ram  $250
https://indianapolis.craigslist.org/sys/d/dell-latitude-e6430-i7-16-gb/6384630737.html
6384630737

Dell ultrabook Intel i7 256gb ssd win10 activated  $200
https://indianapolis.craigslist.org/sys/d/dell-ultrabook-intel-i7-256gb/6420451306.html
6420451306

Laptops for sale  $50
https://cincinnati.craigslist.org/sys/d/laptops-for-sale/6410729719.html
6410729719

Dell Latitude E6530  $450
https://indianapolis.craigslist.org/sys/d/dell-latitude-e6530/6372361863.html
6372361863

DELL LATITUDE E6320 LAPTOP i7 CPU  $269
https://indianapolis.craigslist.org/sys/d/dell-latitude-e6320-laptop-i7/6358155753.html
6358155753

& d1
& q
keith@ada:~$
```
