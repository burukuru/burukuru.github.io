Title: Solr issues with Drupal
Date: 2015-02-24 16:35
Author: Thanh
Category: SysAdmin
Tags: drupal, search, smartos, solr, tomcat, truss
Slug: solr-issues-with-drupal
Status: published

Broken search
=============

One of our clients have been having issue with the search function on
their Drupal site. This full text search was powered by **Solr** behind
the scenes. The issue only only ever occurred when the user was logged
in so it was never flagged up to us.

Recently we've tried to migrate them to a new server and lots of new
changes had to be made; the issue started appearing for all users, even
those that aren't logged in so I decided to take a look.

Symptoms and debugging
======================

The issue only manifested itself with a simple error message:

    The Apache Solr search engine is not available. Please contact your site administrator.

This wasn't really helpful and the Tomcat log files didn't show any
issues. The [Solr
logs](https://skybert.wordpress.com/2009/07/22/how-to-get-solr-to-log-to-a-log-file/)
didn't show the query so I assumed it didn't even hit the Solr app;
manual queries were working fine via the Solr web interface and appeared
in the logs. The next step was to extract the Solr query that Drupal was
running.

The easy way - Drupal
---------------------

If you're running Drupal or any codebase where developers are on hand to
debug the app with you, you can dig into the code and make the app log
or print out the query to the browser.

I came across this very helpful link on how to [debug Solr queries in
Drupal](https://www.drupal.org/node/2240049). In my case, possibly a
different version of Drupal, the file was different:

    # grep -irH drupal_http_request . | grep solr
    sites/all/modules/contrib/apachesolr/Drupal_Apache_Solr_Service.php: $result = drupal_http_request($url, $headers, $method, $content);

I added "drupal\_set\_message(check\_plain(\$url));" and I saw the query
printed in my browser. And it was a huge query...

The hard way - anything else
----------------------------

A lot of the time we would host custom CMS or code that doesn't isn't
maintained by the same developers anymore; in those cases it's much
faster to do the debugging ourselves without digging into the code. If
you're running **SmartOS** and have access to **truss**, this is how to
go about it (strace can probably do something similar in Linux).  
This is actually how I went about it before I realised Drupal probably
has an easier way for me to debug the issue.

    # truss -o /tmp/truss -wall -rall -vall -p $(pgrep httpd)

It will help to have a clone of your server or a dev environment so that
the truss output is less messy to read.  
Run this and do a search on your website. Wait until it finishes and
Ctrl+C truss.

Search for the query:

    # grep -n "G E T / s o l r / s e l e c t " /tmp/truss
    248606:24614: G E T / s o l r / s e l e c t ? f l = i d % 2 C n i d % 2 C t
    870437:24611: G E T / s o l r / s e l e c t ? f l = i d % 2 C n i d % 2 C t

You can also search for 8080 or whichever port Tomcat is running on and
the GET line should be not far below:

    # grep -n AF_INET /tmp/truss.1 | grep 8080
    248599:24614: AF_INET name = 127.0.0.1 port = 8080
    870430:24611: AF_INET name = 127.0.0.1 port = 8080

Go to line 248606 in your truss output and your query should be there,
probably spanning a few send() blocks, it should end with a
"\\r\\n\\r\\n" string.  
After that you should see a recv() block with a response from
Tomcat/Solr. For me, it just showed a "400 Bad Request" error. When I
ran the extracted query with wget, I saw this:

    Resolving localhost (localhost)... 127.0.0.1
    Connecting to localhost (localhost)|127.0.0.1|:8080... connected.
    HTTP request sent, awaiting response... 400 Bad Request
    2015-02-24 15:26:15 ERROR 400: Bad Request.

Once you have the truss output cut down to just the query, you can
remove all the whitespaces, PIDs and system calls; all that will remain
is the actual query that Drupal is running. Mine was quite big:

    # wc /tmp/truss 
    1 9 39733 /tmp/truss

That's 39,733 characters!

Solution was rather straightforward
===================================

So I discovered that the query that Drupal send to Tomcat was humongous.
After a lot of pointless debugging,enabling log files, and looking in
the wrong place, it struck me that it was probably hitting a character
limit. After all the query was not hitting Solr so it must be Tomcat
refusing to process it.

A quick search turned up that the default URL limit on Tomcat was
4096... The setting you need to change is **maxHttpHeaderSize** in
[Tomcat's
server.xml](http://serverfault.com/questions/56691/whats-the-maximum-url-length-in-tomcat).
I set it to 65536 to accommodate some of big queries that were running
and sure enough everything worked fine after a restart!

Retrospectively, I googled the issue again and came across [this
link](https://www.drupal.org/node/443980) which might be helpful it the
above doesn't resolve your issue.
