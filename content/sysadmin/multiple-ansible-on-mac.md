Title: Multiple Ansible versions on Mac
Date: 2016-03-03 00:20
Author: Thanh
Category: SysAdmin
Tags: ansible, testing, debug
Slug: multiple-ansible-versions-on-mac
Status: published

I ran into some regression bugs with the latest version of Ansible and wanted to test to confirm a few things before posting bug reports.
As I run MacOS at work, Ansible is installed from Brew. If you're lucky, you might still have your old versions around:

	$ ls /usr/local/Cellar/ansible/
	1.9.4   2.0.0.2 2.0.1.0

Otherwise you can just clone the branch:
 
	VERSION=stable-2.0.0.1
	git clone -b ${VERSION} --recursive https://github.com/ansible/ansible.git ${VERSION}

and run with the correct PYTHONPATH:

	ANSIBLE_DIR=~/Downloads/ansible/stable-2.0.0.1/
	source ${ANSIBLE_DIR}/hacking/env-setup
	PYTHONPATH="${ANSIBLE_DIR}/lib/:/usr/local/Cellar/ansible/2.0.0.2/libexec/vendor/lib/python2.7/site-packages" ansible-playbook test.yml

env-setup adds the first PATH but the second is specific to the Brew install so you need to add it manually.

If you run the above incorrectly, you will be missing modules and see errors like this:

	Unexpected Exception: No module named yaml
	the full traceback was:

	Traceback (most recent call last):
		File "/Users/thanh/Downloads/ansible/ansible-2.0.0.0-1/bin/ansible-playbook", line 72, in <module>
			mycli = getattr(__import__("ansible.cli.%s" % sub, fromlist=[myclass]), myclass)
		File "/Users/thanh/Downloads/ansible/2.0.0.1/lib/ansible/cli/__init__.py", line 27, in <module>
			import yaml
	ImportError: No module named yaml

or

	Traceback (most recent call last):
 		File "/Users/thanh/Downloads/ansible/ansible-2.0.0.0-1/bin/ansible-playbook", line 39, in <module>
   		from ansible.errors import AnsibleError, AnsibleOptionsError, AnsibleParserError
	ImportError: No module named ansible.errors
