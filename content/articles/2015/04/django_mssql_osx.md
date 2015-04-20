Title: Django & MSSQL on OSX (Yosemite)
Status: published
category: tech
tags: django osx 
slug: django_mssql_osx 

How to connect to MSSQL from Python/Django using pyodbc; The idea is to use a stack that can be easiy replicable on a Linux box (my production target).

<!-- PELICAN_END_SUMMARY -->


> I have 2 macPro, almost identical, I spent 10  minutes to configure django+mssql on the first one, and one day on the second one.

> Here’s a step-by-step intallation that should work in any situation. Maybe I can save you some pain.


The environment:

 - OSX (Yosemite)
 - Django 1.7.7
 - python 2.7
 - pip 6.1.1
 
MSSQL Server:

 - IP: 192.168.1.1
 - port: 1433
 - hostname: DB1
 - database: test1
 - user: username1
 - password: password123
 

Needs:

 - [homebrew](http://brew.sh/) The missing package manager for OS X

 - [FreeTDS](http://www.freetds.org/) an open source ODBC driver. A set of libraries for Unix and Linux that allows your programs to natively talk to Microsoft SQL Server and Sybase databases.
 
 - [UnixODBC](http://www.unixodbc.org/) driver manager, a thin wrapper around the ODBC driver

 - [pyodbc](https://code.google.com/p/pyodbc/) is a Python 2.x and 3.x module that allows you to use ODBC to connect to almost any database from Windows, Linux, OS/X, and more.

 - [django-pyodbc-azure](https://github.com/michiya/django-pyodbc-azure)is a Django Microsoft SQL Server external DB backend that uses ODBC by employing the pyodbc library. It supports Microsoft SQL Server and Azure SQL Database.


##### Step 1: install homebrew

	ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	
##### Step 2: install FreeTDS and unixODBC

	brew install unixodbc  --universal

##### Step 2: install FreeTDS and unixODBC

	brew install freetds --with-unixodbc
	
test the libraries:

	tsql -H 192.168.1.1 -U username1 -P password123 -p 1433
	locale is "en_US.UTF-8"
	locale charset is "UTF-8"
	using default charset "UTF-8"
	1>
	
edit `~/.freetds.conf`

	[db1]
	host = 192.168.1.1
	port = 1433
	tds version = 8.0

test the config

	tsql -S db -U username -P password
	locale is "en_US.UTF-8"
	locale charset is "UTF-8"
	using default charset "UTF-8"
	1>
	
edit `~/.odbc.ini`

	[odbc1]
	Driver = /usr/local/lib/libtdsodbc.so
	Server = 192.168.1.1
	Port   = 1433

and test it

	isql odbc1 username1 password123 -vvvv
	+---------------------------------------+
    | Connected!                            |
    |                                       |
    | sql-statement                         |
    | help [tablename]                      |
    | quit                                  |
    |                                       |
    +---------------------------------------+
    SQL>
	
edit `~/.odbcinst.ini`

	[FreeTDS]
	Driver = /usr/local/lib/libtdsodbc.so
	Setup = /usr/local/lib/libtdsodbc.so
	FileUsage = 1

> Now you can edit your `odbc.ini` and change

	Driver = /usr/local/lib/libtdsodbc.so

to
	
	Driver = FreeTDS

	
##### Step 3: download, edit and install pyodbc

pyodbc usees with unixodbc on Linux, but iODBC drivers on Mac. We need to configure the pyodbc installation such that it works with unixodbc.

First we activate the virtualenv, download pyodbc, edit the setup.py to use unixodbc and install it in the virtualenv

> Note: I use [virtualenv-wrappper](https://virtualenvwrapper.readthedocs.org/en/latest/) to manage virtualenvs


	workon [project_virtualenv] 
	mkdir TEMP
	cd TEMP
	pip install --download . pyodbc
	unzip pyodbc-3.0.7.zip
	cd pyodbc-3.0.7
	
edit these lines in `setup.py`:

	elif sys.platform == 'darwin':
        # OS/X now ships with iODBC.
        settings['libraries'].append('iodbc')


to:

	elif sys.platform == 'darwin':
        # OS/X now ships with iODBC.
        settings['libraries'].append('odbc')
	
build

	python setup.py build_ext --include-dirs=/usr/local/include/ --library-dirs=/usr/local/lib/

and install and remove build dir

	pip install .
   	cdproject
   	rm -fr TEMP


##### Step 4: install django database driver

	pip install django-pyodbc-azure


##### Step 5: Edit your django settings

you have multiple options here:

* you can rely on your `~/odbc.ini` with

```python

	DATABASES = {
 		'default': {
    	    'ENGINE': 'sql_server.pyodbc',
        	'NAME': 'Epweb',
        	'USER': 'username1',
        	'PASSWORD': 'password1'
	        'OPTIONS': {
    	        'host_is_server': True,
        	    'dsn': 'OPWEB'
        	},
        }

```
or

	DATABASES = {
	    'opweb': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'Epweb',
        'USER': wallet.databases.opweb.user,
        'PASSWORD': wallet.databases.opweb.password,
        'HOST': '10.11.40.3',
        'PORT': '1433',
        'AUTOCOMMIT': False,
        'OPTIONS': {
            'host_is_server': True,
        },
    },

Note anyway that FreeTDS driver does not read user credentials from odbc.ini, you have to put them in your `settings.py`


# Some of the errors during the way.....
 
Not sure why I got these errors **only on one of my laptop**. If anyone have the answer please let me know.

* ld: library not found for -lodbc
	
		... build/temp.macosx-10.10-intel-2.7/data/PROGETTI/ONU_WorldFoodProgramme/wfp-commonapi/TEMP/pyodbc-3.0.7/src/sqlwchar.o -L/usr/local/lib/ -lodbc -o build/lib.macosx-10.10-intel-2.7/pyodbc.so
		ld: library not found for -lodbc
		clang: error: linker command failed with exit code 1 (use -v to see invocation)
		error: command 'c++' failed with exit status 1


Solved with `--library-dirs=/usr/local/lib/`


* 	fatal error: 'sql.h' file not found
 
		... TEMP/pyodbc-3.0.7/src/buffer.o -Wno-write-strings -Wno-deprecated-declarations
		In file included from TEMP/pyodbc-3.0.7/src/buffer.cpp:12:
		TEMP/pyodbc-3.0.7/src/pyodbc.h:52:10: fatal error: 'sql.h' file not found
		#include <sql.h>
         ^
		1 error generated.
		error: command 'cc' failed with exit status 1


Solved with `--include-dirs=/usr/local/include/`


* file was built for x86_64 which is not the architecture being linked

		... emp.macosx-10.10-intel-2.7/TEMP/pyodbc-3.0.7/src/pyodbcmodule.o build/temp.macosx-10.10-intel-2.7/TEMP/pyodbc-3.0.7/src/row.o build/temp.macosx-10.10-intel-2.7/TEMP/pyodbc-3.0.7/src/sqlwchar.o -L/usr/local/lib/ -lodbc -o build/lib.macosx-10.10-intel-2.7/pyodbc.so		
		ld: warning: ignoring file /usr/local/lib/libodbc.dylib, file was built for x86_64 which is not the architecture being linked (i386): /usr/local/lib/libodbc.dylib


Solved with: add `--universal` when `brew install unixodbc`


* 'FreeTDS' : file not found 
	
		django.db.utils.Error: ('01000', "[01000] [unixODBC][Driver Manager]Can't open lib 'FreeTDS' : file not found (0) (SQLDriverConnect)")


Solved adding `[FreeTDS]` entry in `odbcinst.ini`



