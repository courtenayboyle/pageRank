This is a set of programs that emulate some of the functions of a 
search engine. They store their data in a SQLITE3 database named
'spider.sqlite'. This file can be removed at any time to restart the
process.  


This program crawls a web site and pulls a series of pages into the
database, recording the links between pages.

In this code, we told it to crawl a website and retrieve a certain number of  
pages. If you restart the program again and tell it to crawl more
pages, it will not re-crawl any pages already in the database. Upon 
restart it goes to a random non-crawled page and starts there. So 
each successive run of spider2.py is additive.


Once you have a few pages in the database, you can run Page Rank on the
pages using the sprank2.py program. You simply tell it how many Page
Rank iterations to run.

If you want to dump the contents of the spider.sqlite file, you can 
see the number of incoming links, the old page rank, the new page
rank, the id of the page, and the url of the page. The spdump23.py program
only shows pages that have at least one incoming link to them. You can dump 
the database periodically to see that page rank has been updated.

You can run sprank2.py as many times as you like and it will simply refine
the page rank the more times you run it.  You can even run sprank2.py multiple
and then go spider a few more pages with spider2.py and then run sprank2.py
to converge the page ranks.

If you want to restart the Page Rank calculations without re-spidering the 
web pages, you can use spreset.py. This will reset all pages to a rank of 1.0.

To visualize the current top pages in terms of page rank,
run spjson2.py to write the pages out in JSON format to be viewed in a
web browser.

You can view this data by opening the file force.html in your web browser.  
This shows an automatic layout of the nodes and links. You can click and 
drag any node and you can also double click on a node to find the URL
that is represented by the node.

This visualization is provided using the force layout from:

http://mbostock.github.com/d3/
