:Title: django and pdbpp
:Status: published
:category: django
:tags: django, pdb
:slug: django_pdbpp


Quick tips how to enable pdb with django

.. PELICAN_END_SUMMARY

`pdbpp`_ is my favourite debugger, I use integrated IDE for my development, but I still
prefer use the command line for most of my daily work.
I find Django sometimes cryptic when some error occurs, (ie. data migrations) this
simple hack, enables pdb when I need, without install third party packages.

It is possible run `python -m pdb manage.py <command>` but this has, sometimes,
some strange side effects, like continue prompting for restarting,
and I loose autocompletion feature (I know, I'm lazy).

In the end I rolled out this custom `manage.py`.

.. code-block:: python

    #!/usr/bin/env python
    import os
    import sys

    if __name__ == '__main__':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wfp_commonapi.settings._%s' % os.environ['USER'])
        from django.core.management import execute_from_command_line

        debug_on_error = '--pdb' in sys.argv
        args = [a for a in sys.argv if a != '--pdb']
        try:
            execute_from_command_line(args)
        except:
            if debug_on_error:
                import pdb, traceback
                type, value, tb = sys.exc_info()
                traceback.print_exc()
                pdb.post_mortem(tb)
            else:
                raise

now I can

.. code-block:: python

    ./manage.py migrate app1 --pdb

and we'll enter in the pdb screen if an error occurs


.. _pdb: https://docs.python.org/2/library/pdb.html
.. _pdbpp: https://bitbucket.org/antocuni/pdb/src
