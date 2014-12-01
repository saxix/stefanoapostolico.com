Title: Playing with Pelican
tags: pelican, python, github pages
category: tech
summary: Pelican and Github pages. Fast and easy blog solution
slug: playing-with-pelican

I spent one day trying to put this blog on Heroku.
Googling on the web many authors explain how to create a static site on Heroku,
and Pelican web site offer a ready to use
[buildpack](http://blog.getpelican.com/using-pelican-with-heroku.html).

Anyway I did not like any of these solutions as all of them
seem recompile and install the full stack (nginx, pelican, python....)

I moved to a more pratical and easy to implement solution:
[GitHub pages](https://pages.github.com/) and [Pelican](http://docs.getpelican.com/en/3.5.0).

### Install Pelican

To install Pelican and other Python package dependencies in a virtual environment, 
I followed the instructions in the official 
[Pelican documentation](http://pelican.readthedocs.org/en/3.5.0/quickstart.html).

``` bash
   
pip install pelican Markdown typogrify
pelican-quickstart

```

I enabled article pagination so that I didn't end up with all the posts on a single 
page. The ``Makefile`` is incredibly useful, so I enabled that. 
It allows you to compile the website with ``make html`` and check it live with ``make serve``. 

Because I want to use Github pages I answered NO to all the questions about
``Dropbox``, ``S3``, ``FTP`` and ``SSH`` anyway the related code is still 
in the ``Makefile`` so I removed it manually.

### Configure plugins

To configure plugins simply clone pelican-plugins as git submodule with

    git add submodule https://github.com/getpelican/pelican-plugins
    git submodule update  --init --recursive
    
and enable what you like in ``pelicanconf.py``

```python
    PLUGIN_PATHS = ['pelican-plugins']
    PLUGINS = ['interlinks',
               'pelican_fontawesome',
               'related_posts',
               'summary',
               'sitemap',
               'simple_footnotes']
```


### Configure Github

For Github you need to put the domain of your site inside a CNAME (must be uppercase)
file at the root of your site. 


More details how to configure your domain can be found 
[here](http://docs.getpelican.com/en/3.5.0/tips.html#extra-tips) (Tip #2),
[here](https://help.github.com/articles/about-custom-domains-for-github-pages-sites/)
and [here](https://help.github.com/articles/my-custom-domain-isn-t-working/)

For my configuration I used 

``content/extras/CNAME``

```
stefanoapostolico.com
```

``pelicanconf.py``

```python
    
    STATIC_PATHS = ['images', 'extras/README.rst', 'extras/CNAME', 
    'extras/robots.txt']

    EXTRA_PATH_METADATA = {
        'extras/README.rst': {'path': 'README.rst'},
        'extras/CNAME': {'path': 'CNAME'},
        'extras/robots.txt': {'path': 'robots.txt'},
    }

```

### Minor improvements

#### Get metadata from path

To store articles in a structure like 
``category/YEAR/MONTH/DAY-slug`` so I updated my ``pelicanconf.py`` as 


```python
   PATH_METADATA = '\A(?P<category>[^/]+)/(?P<date>\d{4}/\d{2}/\d{2})-(?P<slug>.*)(.md|.rst)'
```

You can always override date, slug and category in your post.

#### Serve file with different path

To serve your articles with url like ``/YEAR/MONTH/DAY/slug.html``

```python
    ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
    ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
```

You must set both the setting.



you can see the result [here](https://github.com/saxix/stefanoapostolico.com)



