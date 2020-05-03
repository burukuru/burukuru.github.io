Title: SMTP authentication in Exim
Date: 2015-01-28 01:56
Author: Thanh
Category: Linux
Tags: exim
Slug: smtp-authentication-in-exim
Status: published

#### No more Google SMTP for your aliases

Since August last year, Google have grandfathered a feature in GMail
that allows you to create aliases in your account and send emails as
those aliases from their SMTP servers:

<http://googlesystem.blogspot.co.uk/2014/08/external-addresses-no-longer-use-gmail.html>

For any new aliases, you will need to provide your own SMTP servers.  
If you have a VPS of some sort, this is how you can set up simple SMTP
authentication in Exim to pipe your emails through your server and keep
using the Google web interface.

#### SMTP Authentication

LOGIN and PLAIN auth differs in the fact that LOGIN will prompt for the
username/password explicitely whereas in PLAIN the client is expected to
send both in one blob.  
Practically the only difference is an additional null byte at the
beginning of the LOGIN blob send to the server.

##### LOGIN

How to set up simple SMTP LOGIN auth with SHA1 (alternative is crypt or
MD5..):

exim.conf file (based on a  Ubuntu template):

    ...
    CONFDIR = /etc/exim4/
    ...
    begin authenticators

    LOGIN:
    driver = plaintext
    public_name = LOGIN
    server_prompts = <| Username: | Password:
    server_advertise_condition = ${if def:tls_cipher }
    server_condition = "${if crypteq {$auth2}{\\\{sha1\\\}${extract{1}{:}{${lookup{$auth1}lsearch{CONFDIR/passwd}{$value}{*:*}}}}}{1}{0}}"
    server_set_id = $auth1

passwd file:

    username:[PASSWORD HASH]

How to generate password hash:

    perl -MDigest::SHA=sha1_hex -e 'print sha1_hex($ARGV[0]),"\n"' [PASSWORD]

To test this, you need to encode the username/pass in base64:

    # cat encode.pl
    use MIME::Base64;
    printf ("%s", encode_base64(eval "\"$ARGV[0]\""));
    # perl encode.pl 'username\0password'
    dXNlcm5hbWUAcGFzc3dvcmQ=
    ...
    # exim -bh localhost
    > ehlo test
    > auth login dXNlcm5hbWUAcGFzc3dvcmQ=

##### PLAIN

If you'd rather have a PLAIN auth, just change the snippet in exim.conf
to:

exim.conf file

    ...
    CONFDIR = /etc/exim4/
    ...
    begin authenticators

    PLAIN:
    driver = plaintext
    public_name = PLAIN
    server_advertise_condition = ${if def:tls_cipher }
    server_condition = "${if crypteq {$auth3}{\\\{sha1\\\}${extract{1}{:}{${lookup{$auth2}lsearch{CONFDIR/passwd}{$value}{*:*}}}}}{1}{0}}"
    server_set_id = $auth2

to test, run:

    # perl encode.pl '\0username\0password'
    AHVzZXJuYW1lAHBhc3N3b3Jk
    # exim -bh localhost
    > ehlo test
    > auth plain AHVzZXJuYW1lAHBhc3N3b3Jk

##### SSL

Test with SSL by using this instead of 'exim -bh':

    openssl s_client -connect server.com:465

#### Links

<http://www.exim.org/exim-html-current/doc/html/spec_html/ch-smtp_authentication.html>

<http://www.exim.org/exim-html-current/doc/html/spec_html/ch-string_expansions.html>

<https://www.debian-administration.org/article/280/HowTo_Setup_Basic_SMTP_AUTH_in_Exim4>
