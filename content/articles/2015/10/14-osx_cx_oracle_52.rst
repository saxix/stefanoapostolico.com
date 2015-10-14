:Title: cx-Oracle 5.2 on OSX (El Capitan)
:Status: published
:category: tech python
:tags: cx_Oracle SIP
:slug: install_cxoracle_52_on_osx


Install cx-Oracle 5.2 on OSX (El Capitan), mostly for my reference

.. PELICAN_END_SUMMARY

What we install
---------------

- Oracle Instant Client 64bit 11.2.0.4.0
- cx-Oracle 5.2


.. code-block:: bash

    export $ORACLE_HOME=/data/oracle/instantclient_11_2
    mkdir -p $ORACLE_HONE
    
    export DYLD_LIBRARY_PATH=$ORACLE_HOME
    export LD_LIBRARY_PATH=$ORACLE_HOME

    unzip 'instantclient*.zip' -d $ORACLE_HOME/..
    
    ln -s $ORACLE_HOME/libclntsh.dylib.11.1 $ORACLE_HOME/libclntsh.dylib
    pip install cx-Oracle


Links
-----

- `Oracle Instant Client Downloads <http://www.oracle.com/technetwork/topics/intel-macsoft-096467.html>`_
