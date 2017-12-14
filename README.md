**craigslist_forsale_notify** is a small python3 script (running under Linux on the command line) which aims to replace the Craigs List email notification functionality of 'saved searches' for personal use of the "For Sale" category. This script is designed for and tested on Linux OS only, but can likely be easily modified for other OS's. Support for English only.

Since CraigsList does not provide a public API, this script uses scraping to capture information. So this script will need to be modified if CraigsList changes their page/data structure.

#### Overview of how it works:
1. You must setup the requirements on your system.
2. You must edit the script to include the location and nearby areas you want to search, plus your correct SMTP server and email information.
3. Run the script (from the command line or for use with Crontab) with your search terms as command line arguments (separated by spaces).
4. The script uses Requests to download the search results page then uses BeautifulSoup to scrape for the pid, item, price, and url of the results.
5. The script then uses SMTP to send the results to your provided email address.
6. The script also creates/appends a file which keeps track of the pid's so it won't send you them a second time on future searches.

#### Benefits:
1. Run it when and as many times as you like.  By contrast, the CraigsList 'Saved searches' function has an odd algorithm for when it runs, and you have no control.
2. Won't repeat results as it keeps track of which items you have already seen.  By contrast, the CraigsList 'Saved searches' function will keep sending you the same items.


#### Requirements:
1. Of course you need an email address and the correct SMTP info to access it.
2. Python3 running on Linux.
3. These Python modules properly installed (generally with pip):  
  * requests
  * BeautifulSoup4
  * lxml.  


4. A path to where the script can write to a file.

#### Example of how I use this script:
There are a few items which appear on CraigsList infrequently that I like to follow over the course of several months. Here is an example of the content of my SEARCHES_FILE which I keep in my home directory:

```  
keith@ada:~$ cat cl_searches.txt
(tektronix | agilent | hp) (oscilloscope* | scope*) -buy
"hemp oil" | "hemp soap"
minolta autocord
hasselblad
"bay 1 filter"
```  
If I wanted to add a search for, say, concert tickets, I could just do this at the command line:

```
keith@ada:~$ echo \"pink floyd\" \"concert tickets\">> cl_searches.txt
```  
I can run the script manually at anytime, or I can also put it into a crontab for scheduling.

Or just run it from the command line whenever:
```  
keith@ada:~/code/cl$ python3 cl.py "pink floyd" "concert tickets"
```  
