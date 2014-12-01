Title: Deploying Django app with Ansible on Amazon AWS 
tags: python, django, aws, ansible, ngnix, uwsgi
status: draft

<!-- PELICAN_END_SUMMARY -->


### Prerequisites

- Amazon EC2 instance
- working django app :)

### Why Ansible?

It’s agentless.  Unlike Puppet, Chef, Salt, etc.. Ansible operates only over SSH (or optionally ZeroMQ), so there’s none of that crap PKI that you have to deal with using Puppet.

It’s Python. I like Python.  I’ve been using it far longer than any other language. 

### Our stack

- ubuntu-trusty-14.04-amd64-server-20140927 (ami-b83c0aa5)
- python 2.7.8
- ngnix
- uwsgi
- django 1.7.1


All the stack will be compiled from source code in local directory to be totally decoupled from the system environment.

I used to compile most of my stack from scratch, I started doing this some year ago when I was forced to use a very old RHEL and most of the required software was not available from the vendor's repository


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

### Create provision.yml











