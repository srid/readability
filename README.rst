readability
===========

A Python implementation of the algorithm__ used in arc90's `readability
bookmarklet`_::

    >>> import urllib
    >>> import readability
    >>> url = 'http://www.nytimes.com/2010/09/07/health/views/07mind.html'
    >>> html = urllib.urlopen(url).read()
    >>> print readability.readable(url, html)[0]

.. WARNING:: The above API **may change** before release.

To directly open the readable version of a URL in the web browser::

    $ readability -b http://blog.doughellmann.com/2007/04/pymotw-linecache.html

readability.py is not released yet. To install the development version::

    $ pip install -e git://github.com/srid/readability.git#egg=readability

Credits
-------

``readability.py`` adds several bug fixes and features to ``hn.py`` in the
`Readable Feeds`_ project that adapted the original `hn.py`_ by Nirmal Patel.
readability.py retains the original license (**GPL3**) chosen by its
predecessors.


.. __: http://code.google.com/p/arc90labs-readability/downloads/detail?name=readability.js&can=2&q=
.. _`readability bookmarklet`: http://lab.arc90.com/experiments/readability/
.. _`hn.py`: http://nirmalpatel.com/fcgi/hn.py
.. _`Readable Feeds`: http://github.com/scyclops/Readable-Feeds
