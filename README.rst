***************
django-livejs2
***************

Integrates `live.js`_ into your django project. 

There is already a project named django-livejs, so I added "2" to the name to avoid conflict. (Additionally I think my version is better than that one :P )

Installation
***************

1. Either run ``python setup.py install`` or use ``pip`` to install the package.

2. Edit your ``settings.py`` to add ``'django_livejs2.middleware.LiveJsMiddleware'`` to ``MIDDLEWARE_CLASSES``. Also add  ``'django_livejs2'`` to ``INSTALLED_APPS`` if you want to use the shipped `live.js`_.

Usage
***************

Just visit any page with ``live=1`` in query string to enable the module. When enabled, `live.js`_ will be included in every HTML page. The module will also make all files uncacheable by browser, so that any updates to static files will have effect immediately. (Without that Firefox may cache static files for 1 minute)

Disabling is also easy, visit any page with ``live=0`` in query string and you are done. 

Note: If ``settings.DEBUG`` is not ``True``, the module will be completely disabled since it is not really useful in production environment.

Settings
***************

LIVEJS2_SCRIPT_SRC
------------------

If you want to use a custom version of `live.js`_, set this to URL of the script.

.. _live.js: http://livejs.com/
