init:
	python bootstrap.py
	bin/buildout

test:
	bin/py.test -x -v test/test.py


.PHONY: init test