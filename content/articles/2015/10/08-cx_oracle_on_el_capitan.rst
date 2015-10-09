:Title: cx_Oracle and System Integrity Protection (El Capitan)
:Status: published
:category: tech python 
:tags: cx_Oracle SIP 
:slug: install_cx_oracle_with_sip_enabled


With the relase of El Capitan, Apple has enabled a new default security
feature named System Integrity Protection, also called rootless.
This may cause some apps, utilities, and scripts to not function at all, 
even with sudo privelege, root user enabled, or admin access. 
Oracle drivers seems one the these.

Not interest in the long story? Here the `trick <#solution>`_ !!!


System Integrity Protection 
===========================

`System Integrity Protection <https://developer.apple.com/library/prerelease/mac/releasenotes/MacOSX/WhatsNewInOSX/Articles/MacOSX10_11.html>`_ 
is aimed at preventing Mac OS X compromise by malicious code, 
whether intentionally or accidentally, and essentially what SIP does is lock down 
specific system level locations in the file system while simultaneously 
preventing certain processes from attaching to system-level processes.

For System Integrity Protection locks down the following system level directories:

    - /System
    - /sbin
    - /usr (with the exception of /usr/local)

There are a lot of infos how to disable rootless, 
what we want to achieve is to let cx_Oracle works without disable SIP.


Let try to see what happen when we try to use cx_Oracle.

.. code-block:: bash

    $ ./manage.py inspectdb --database=pasport
    Traceback (most recent call last):
      File "./manage.py", line 12, in <module>
        execute_from_command_line(sys.argv)
      ...
      ...
      File "TEST_VIRTUALENV/lib/python2.7/site-packages/django/db/backends/oracle/base.py", line 47, in <module>
        raise ImproperlyConfigured("Error loading cx_Oracle module: %s" % e)
    django.core.exceptions.ImproperlyConfigured: Error loading cx_Oracle module: dlopen(TEST_VIRTUALENV/lib/python2.7/site-packages/cx_Oracle.so, 2): Library not loaded: /ade/b/3071542110/oracle/rdbms/lib/libclntsh.dylib.11.1
      Referenced from: TEST_VIRTUALENV/lib/python2.7/site-packages/cx_Oracle.so
      Reason: image not found
 
      
uh oh!!
=======
 
 
cx_Oracle seems not able to find `/ade/b/3071542110/oracle/rdbms/lib/libclntsh.dylib.11.1`.
Now, I have no idea where this path come from, anyway I have `libclntsh.dylib.11.1` in my
``$ORACLE_HOME`` so I have to tell cx_Oracle to see there. Checking with otool confirm that

.. code-block:: bash

    $ otool -L TEST_VIRTUALENV/lib/python2.7/site-packages/cx_Oracle.so
    TEST_VIRTUALENV/lib/python2.7/site-packages/cx_Oracle.so:
        /ade/b/3071542110/oracle/rdbms/lib/libclntsh.dylib.11.1 (compatibility version 0.0.0, current version 0.0.0)
        /usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1225.1.1)

we need to relync binaries they do not try to access avoided location; 
to achieve this we use to command line tools `otool`_ and `install_name_tool`_
 

.. code-block:: bash
    
    install_name_tool -change /ade/b/3071542110/oracle/rdbms/lib/libclntsh.dylib.11.1 $ORACLE_HOME/$baselib TEST_VIRTUALENV/lib/python2.7/site-packages/cx_Oracle.so

check the result

.. code-block:: bash

    $ otool -L TEST_VIRTUALENV/lib/python2.7/site-packages/cx_Oracle.so
    TEST_VIRTUALENV/lib/python2.7/site-packages/cx_Oracle.so:
        /data/oracle/instantclient_11_2/libclntsh.dylib.11.1 (compatibility version 0.0.0, current version 0.0.0)
        /usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1225.1.1)

try again

.. code-block:: bash

    $ ./manage.py inspectdb --database=pasport
    ...
    ...
    raise ImproperlyConfigured("Error loading cx_Oracle module: %s" % e)
    django.core.exceptions.ImproperlyConfigured: Error loading cx_Oracle module: dlopen(/data/VENV/capi/lib/python2.7/site-packages/cx_Oracle.so, 2): Library not loaded: /ade/dosulliv_ldapmac/oracle/ldap/lib/libnnz11.dylib
    Referenced from: /data/oracle/instantclient_11_2/libclntsh.dylib.11.1
    Reason: image not found

mmmm, same problem with oracle binaries, we need to apply the same patch.

.. html::
    <a name="solution">

The trick
=========

A very simple script that allow you to easily patch the files. 
It accept two arguments, ``-o`` and ``-e`` respectively to patch oracle binaries 
and/or ``cx_Oracle.so`` in the active virtualenv

You only need to patch oracle binaries once, cx_Oracle need 
to be patched for each virtualenv (if many)

 
.. code-block:: bash

    $ ./cxOracleSIP.sh -o -e

Download `cxOracleSIP.sh <../../../files/cxOracleSIP.sh>`_


The script
==========

.. code-include:: ../../../files/cxOracleSIP.sh



References
----------

 - `How to copy (and relink) binaries on OSX using otool and install_name_tool <http://thecourtsofchaos.com/2013/09/16/how-to-copy-and-relink-binaries-on-osx/>`_

 - `Oracle sqlplus and instant client on Mac OS/X without DYLD_LIBRARY_PATH <http://blog.caseylucas.com/2013/03/03/oracle-sqlplus-and-instant-client-on-mac-osx-without-dyld_library_path/>`_

 - `Creating working dylibs <http://qin.laya.com/tech_coding_help/dylib_linking.html>`_

 - `How to Disable System Integrity Protection (rootless) in OS X El Capitan <http://osxdaily.com/2015/10/05/disable-rootless-system-integrity-protection-mac-os-x/>`_

.. _otool: http://www.unix.com/man-page/osx/1/otool/
.. _install_name_tool: http://www.unix.com/man-page/osx/1/install_name_tool/

