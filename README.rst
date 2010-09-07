readability
===========

A Python module arc90's readability.js that powers the readability bookmarklet::

    >>> import urllib
    >>> import readability
    >>> url = 'http://www.nytimes.com/2010/09/07/health/views/07mind.html'
    >>> html = urllib.urlopen(url).read()
    >>> print readability.grabContent(url, html)

Credits
-------

Originally implemented as `hn.py`_ by Nirmal Patel; later adapted Andrew Trusty
in his `Readable Feeds`_ project.

.. _`hn.py`: http://nirmalpatel.com/fcgi/hn.py
.. `Readable Feeds`: http://github.com/scyclops/Readable-Feeds
