Title: Some useful filters for parsing JSON with jq
Date: 2015-05-06 14:45
Author: Thanh
Category: Uncategorized
Slug: some-useful-filters-for-parsing-json-with-jq
Status: draft

I've been told [jq](http://stedolan.github.io/jq/) is the new cool JSON
parser. As I used to use the 'json' command that came from npm, I had to
adapt my scripts slightly.

jq -r .

Re-arrange the output:

jq -r '.[] | {name: .name, dob: .dob} | join (" ")'

jq -r '[.options[] | select(.name=="blah")'

 

 
