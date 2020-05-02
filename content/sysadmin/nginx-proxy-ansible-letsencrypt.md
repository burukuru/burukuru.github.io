Title: Nginx proxy with Ansible and letsencrypt for multiple domains
Date: 2016-08-25 12:38
Author: Thanh
Category: SysAdmin
Tags: nginx, proxy, ansible, letsencrypt, ssl
Slug: nginx-proxy-ansible-letsencrypt
Status: published

Say you're running an nginx proxy and need to set up multiple domains with different backends.

Using: https://github.com/thefinn93/ansible-letsencrypt/

proxy.yml:

	- hosts: proxy
	  vars:
	    letsencrypt_webroot_path: /var/www/letsencrypt/
	    letsencrypt_email: foo@bar.com
	    letsencrypt_cert_domains:
	      - site.com
	      - www.site.com
	      - othersite.org
	    letsencrypt_renewal_command_args: '--renew-hook "systemctl restart nginx"'
	  roles:
	    - { role: ansible-letsencrypt, tags: letsencrypt }
	    - { role: nginx, tags: nginx }
			

In your nginx role:

nginx.conf.j2:

	http {
	...
	    ssl_certificate /etc/letsencrypt/live/{{ letsencrypt_cert_domains[0] }}/fullchain.pem;
	    ssl_certificate_key /etc/letsencrypt/live/{{ letsencrypt_cert_domains[0] }}/privkey.pem;
	...
	}
	
site.conf.j2:

	server {
	
	  listen 80;
	  listen 443;
	
	  server_name site.com;
	
	  location /.well-known/acme-challenge {
	    add_header  X-Robots-Tag "noindex, nofollow, nosnippet, noarchive";
	    root /var/www/letsencrypt/;
	  }   
	}
