Title: Finding out your Solr version
Date: 2015-10-01 10:47
Author: Thanh
Category: SysAdmin
Tags: solr, tomcat
Slug: finding-out-your-solr-version
Status: published

I can never remember how to do this without the GUI so here is the quick
command to detect the Solr version you're currently running:

    wget -q -O- localhost:8080/solr/admin/registry.jsp | grep -E "spec-version|impl-version"

A helpful StackOverflow
link:<https://stackoverflow.com/questions/2395089/how-do-i-find-out-version-of-currently-running-solr>
