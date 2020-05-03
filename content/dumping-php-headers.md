Title: Dumping PHP headers
Date: 2016-03-07 16:43
Author: Thanh
Category: SysAdmin
Tags: php, debugging
Slug: dumping-php-headers
Status: published

I read this somewhere and want to keep it around.

Sometimes I need to debug HTTPS/header issues in a load balanced environment.

Here's how to dump all the headers in PHP:

	/* {DocumentRoot}/headers.php
	Show all values defined on $_SERVER */
	<?php
		 while (list($var,$value) = each ($_SERVER)) {
				echo "$var => $value <br />";
		 }
	?>
