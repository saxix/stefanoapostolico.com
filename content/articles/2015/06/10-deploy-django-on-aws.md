Title: Amazon and full Django stack with Ansible
tags: python, django, aws, ansible, ngnix, uwsgi
status: draft

howto deploy django project based on nginx,uwsgi,postgres on Amazon Ec2, using Ansible
<!-- PELICAN_END_SUMMARY -->


### Prerequisites

- Amazon EC2 instance
- working django app :)

### Why Ansible?

It’s agentless.  Unlike Puppet, Chef, Salt, etc.. Ansible operates only over SSH (or optionally ZeroMQ), so there’s none of that crap PKI that you have to deal with using Puppet.

It’s Python. I like Python.  I’ve been using it far longer than any other language. 

### Our stack

- ubuntu-trusty-14.04-amd64-server-20140927 (ami-b83c0aa5)
- python
- ngnix
- uwsgi
- django
- postgres

> As example we'll deploy a django project named `myproject`

**Note**

- We install our local code (no git, no pypi), it's very easy update the script to use git/pypi

- we use setuptools to define our requirements 


### Installing Ansible


	pip install ansible

### Enable your certificate 

temporary enable it with `ssh-agent`

	ssh-agent 
	ssh-add <YOUR_AWS_CETIFICATE>
	
or pass to ansible command line

	--private-key <YOUR_AWS_CETIFICATE>
	
### Create Ansible inventory

Create `<PROJCT_ROOT>/deploy/hosts` and put the pubilc IP of your instance in it (example). This file is called [inventory](http://docs.ansible.com/intro_inventory.html) in Ansible terminology.

	[webservers]
	11.22.333.44 

To retrieve your connection string browse <https://console.aws.amazon.com/ec2/v2/home?region=eu-central-1#Instances> and click `Connect` button

![me](/images/deploy-django-on-aws/aws-connect.png)


	
### Test connection

	ansible all -m ping -u <USER>
	
you should receive a respose like:

	<USER>@11.22.333.44 | success >> {
 	   "changed": false,
    	"ping": "pong"
	}


> We create the full stack in one single machine, change the scripts to deploy on dedicated hardware for each tier will need minor improvements to the configuration

### Create ansible directory tree

In the root of our project (same level of `setup.py`) create this directory tree:

	deploy
	+-- templates
		--- nginx.conf
		--- settings.py
		--- uwsgi.ini
		--- uwsgi.conf
	+-- roles
	   	+-- admin
	    	+-- tasks
	    		--- main.yml
	    	+-- templates
	    		--- main.yml
	    	+-- vars
	    		--- main.yml
	+--	vars
		-- global.yml
		-- provision.yml
		-- application.yml
	+-- tasks
	   	--- perms.yml
	-- provision.yml
	-- hosts
	-- deploy.yml
	
#### Directory: vars
	
This directory contains most of the [Variables](http://docs.ansible.com/playbooks_variables.html#defaulting-undefined-variables) used by our deployemet

**vars/global.yml**

```
prefix: "/data"
virtualenv: "{{prefix}}/myproject-venv"
config:
	group: "www-data"
```	
**vars/provision.yml**

```
nginx:
  server_name: default
  http_port: 80
  loglevel: error # debug, info, notice, warn, error, crit, alert, emerg
  static_root: "{{prefix}}/var/static"
  media_root: "{{prefix}}/var/media"

uwsgi:
  socket: '{{prefix}}/run/uwsgi.sock' # WARNING change nginx.upstream
  processes: 2


system_packages:
  - wget
  - curl
  - nginx
  - python
  - git
  - libpq-dev
  - libzmq-dev
  - postgresql
  - postgresql-contrib
  - postgresql-client
  - python-dev
  - python-setuptools
  - python-virtualenv

```	

**vars/application.yml**

```
package:
  name: myproject
  version: 0.1dev

install: "file://{{prefix}}/myproject-0.1.0dev.tar.gz#egg=myproject[postgres]"

django:
  database:
    name: myproject
  settings: "settings_production"
  wsgi: "myproject.wsgi"

```	

## Writing our first playbook: provision.jaml

with this playbook will setup the host, installing and onfiguring all the required servers:

 - ngnix
 - uwsgi
 - postgres
 
 start the playbook
 
 
 ```
---

- hosts: webservers
  gather_facts: no

  remote_user: "{{ remote_user }}"

  vars_files:
    - vars/global.yml
    - vars/provision.yml
    - vars/application.yml

 ``` 		














