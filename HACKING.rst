Development setup
=================

Ensure that git submodules are present::

    $ git submodule init && git submodule update

Install fabric and run::

  $ fab init
  $ fab test
  $ bin/readability

Release HOWTO
=============

To make a release, 

  1) Update release date/version in NEWS.txt and setup.py
  2) Run 'python setup.py sdist'
  3) Test the generated source distribution in dist/
  4) Upload to PyPI: 'python setup.py sdist register upload'
  5) Increase version in setup.py (for next release)

