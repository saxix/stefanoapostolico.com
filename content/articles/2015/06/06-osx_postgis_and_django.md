Title: PostGIS, PostgreSQL, and Django on OS X
Status: published
category: tech
tags: django postgis postgresql
slug: osx_postgis_and_django

Here's how I got through the installation and configuration of PostGIS on OS X (10.10 Yosemite).

<!-- PELICAN_END_SUMMARY -->

This post is mainly for my reference. I spent too much time to find a clear reproducible way to achieve the result.


Here's what finally worked for me.


### The stack

- Postgresql 9.4.3
- PostGIS  2.1.7
- Python 2.7
- Django 1.7


## Install PostGIS

I'm not sure I could have actually accomplished this without Homebrew. It really is a great package management tool for OS X. It handles dependencies with no pain at all.

#### get package info

	brew info postgis

this produce something like (partial):	
	
```
postgis: stable 2.1.7, HEAD
Adds support for geographic objects to PostgreSQL
http://postgis.net
Not installed
```	

#### Install PostGIS

If the version you got does not match this post, try with:

    brew tap postgis
    brew search postgis
	brew install homebrew/versions/postgis20
	
otherwise:

	brew install postgis

Homebrew will install both PostGIS and PostgreSQL, check it with

	brew info postgres
	brew info postgis

the default data dir `/usr/local/var/postgres` is owned by `root` and I prefre to run my database as non privileged user, first I need to chown the directory

	sudo chown sax /usr/local/var/postgres 

#### Initialize 

	initdb /usr/local/var/postgres  -E utf8

#### Launch postgres

	pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start

To do not receive annoying messages during my daily activities I also create the standard ``postgres`` superuser

	createuser -s -r postgres
	


## PostGIS Functions and Template

PostGIS essentially is a table a couple of databse views and a many functions. You need to create a "template" database to store all of them.


Create the database that we use as template for any 

	createdb template_postgis
	psql -f /usr/local/share/postgis/postgis.sql template_postgis
	psql -f /usr/local/share/postgis/spatial_ref_sys.sql template_postgis



## Create Django database

	psql -c 'CREATE DATABASE wfp_commonapi_gis;' -U postgres;
	psql -d gis_example -c 'CREATE EXTENSION postgis;' -U postgres;

or

	createdb -E UTF8 PIPPO -T template_postgis


> ***NOTE:*** Do not run django test before you create the "real" PostGIS database (at least with pytest) or you get a ``OperationalError: FATAL:  database "DBNAME" does not exist``. Seems that Django is not able to create a PostGIS test database if the original one does not exists.



## Final steps

#### Make PostGIS start automatically

This is done following the hint on bottom of `brew info postgres` output

	ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents 
	launchctl load ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist


#### Put everything togheter


```
#!/usr/bin/env bash

PGDATA="/usr/local/var/postgres"
LOG="/usr/local/var/postgres/server.log"

brew install postgis || exit 1
sudo chown sax ${PGDATA}  || exit 1
initdb ${PGDATA} -E utf8  || exit 1

pg_ctl -D ${PGDATA} -l ${LOG} start -w || exit 1

createuser -s -r postgres  || exit 1

createdb template_postgis || exit 1

psql -f /usr/local/share/postgis/postgis.sql template_postgis  || exit 1
psql -f /usr/local/share/postgis/spatial_ref_sys.sql template_postgis  || exit 1

pg_ctl status

```





