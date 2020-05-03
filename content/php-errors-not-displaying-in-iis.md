Title: PHP errors not displaying in IIS
Date: 2012-05-18 19:32
Author: Thanh
Category: SysAdmin
Tags: iis, php
Slug: php-errors-not-displaying-in-iis
Status: published

A customer called in today saying that their site is not working after
re-pointing the DNS. No changes have been made in a week and it was
working fine before. Typical.

So I turned on Firebug and notice it's a 500 error. Logged into the
server and saw it's a WordPress instance running with PHP on IIS. Great!
For some reason the pages in the browser are completely blank. I loaded
up the page from a local browser and the same thing happens. I double
checked that detailed errors messages have been enabled in IIS and they
were. Very strange.

The IIS log was as unhelpful as ever so I turned to DuckDuckGo (nearly
wrote 'Google' there but I switched my search engine recently). Now I'm
not usually used to WordPress in IIS so didn't think of checking the
php.ini file; later on it turned out that error messages option was not
set  but it's supposedly on by default but errors just decided not to
show.

Cutting to the chase, I dropped the following into the PHP file:

    ini_set('display_errors',true);

This uncovered  a plugin was installed twice and WordPress was having
none of that. Renamed the file and all was well again. Thanks to [Sadi
from
iis-answers.com](http://www.iis-answers.com/microsoft/IIS/33603808/iis-not-showing-php-errors.aspx)
for pointing that out!
