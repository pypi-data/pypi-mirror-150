django4-js-urls
###############

.. image:: https://img.shields.io/pypi/l/django4-js-urls.svg
    :target: https://pypi.python.org/pypi/django4-js-urls/
    :alt: License

.. image:: https://img.shields.io/pypi/pyversions/django4-js-urls.svg
    :target: https://pypi.python.org/pypi/django4-js-urls

.. image:: https://img.shields.io/pypi/v/django4-js-urls.svg
    :target: https://pypi.python.org/pypi/django4-js-urls/
    :alt: Latest Version

.. .. image:: https://travis-ci.org/impak-finance/django-js-urls.svg?branch=master
..     :target: https://travis-ci.org/impak-finance/django-js-urls

.. .. image:: https://codecov.io/gh/impak-finance/django-js-urls/branch/master/graph/badge.svg
..   :target: https://codecov.io/gh/impak-finance/django-js-urls

.. |

**Django4-js-urls** is a lightweight Django application allowing to easily get absolute path
references matching given URL names and optional parameters on the client side - just like
`reverse <https://docs.djangoproject.com/en/dev/ref/urlresolvers/#reverse>`_ does, but in a
Javascript fashion.

.. contents:: Table of Contents
    :local:

Main requirements
=================

Python 3.8+, Django 3.2+.

Installation
============

To install Django4-js-urls, please use pip_ (or pipenv_) as follows:

.. code-block:: shell

    $ pip install django4-js-urls

Once installed you just need to add ``js_urls`` to ``INSTALLED_APPS`` in your project's settings
module:

.. code-block:: python

    INSTALLED_APPS = (
        # other apps
        'js_urls',
    )

URLs that are included in the Javascript helper tool are configured using a single ``JS_URL``
setting. This setting can embed URL namespaces or specific URL names that should be included in the
generated Javascript file. For example:

.. code-block:: python

    JS_URLS = (
        'admin',
        'blog:article_list',
        'blog:article_detail',
    )

**Important:** only URLs defined in this setting will be included in the generated Javascript file.
You don't want to expose *all* the URLs of your Django project in a Javascript file.

Then you can include the view responsible for generating the Javascript file in your URLs root
module:

.. code-block:: python

    from js_urls.views import JsUrlsView

    urlpatterns = [
        # other urls
        url('js-urls/$', JsUrlsView.as_view(), name='js_urls'),
    ]

And finally you can include the Javascript script in your base template as follows:

.. code-block:: html

    <script src="{% url 'js_urls' %}" type="text/javascript"></script>

Usage
=====

URLs included in the generated Javascript file can be used in your scripts by using the
``window.reverse`` function. Here are some example:

.. code-block:: javascript

    const url1 = window.reverse('home');
    const url2 = window.reverse('blog:article_list');
    const url3 = window.reverse('blog:article_detail', articleId);
    const url4 = window.reverse('blog:article_detail', [articleId, ]);
    const url5 = window.reverse('blog:article_detail', { pk: articleId });

Settings
========

JS_URLS
-------

Default: ``[]``

The ``JS_URLS`` setting allows to define URL namespaces or specific URL names that should be
included in the generated Javascript file.

JS_URLS_FUNCTION_NAME
---------------------

Default: ``'reverse'``

The ``JS_URLS_FUNCTION_NAME`` setting allows customize the name of the function used to reverse
URLs on the client side. This function is made available through the ``window`` global object.

Authors
=======

impak Finance <tech@impakfinance.com>.

License
=======

MIT. See ``LICENSE`` for more details.

.. _pip: https://github.com/pypa/pip
.. _pipenv: https://github.com/pypa/pipenv
