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

Old algorithm
-------------

Unfortunately this project, like others, uses an older version of the
readability algorithm, Viz.

`Matt
<http://blog.interstellr.com/readability-in-python-using-lxml#comment_6488354>`_:
*[...]  the readability.js file that can be downloaded from the "downloads"
section of the Google Code project is a year and a half old and only 8.9KB
(about 250 loc), while the trunk version (presumably similar to what's used in
the bookmarklet) has expanded to a whopping 73.5KB and 1825 loc.*

Ideally, we should port this project to use the same algorithm as the
bookmarklet.

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
