init:
	python bootstrap.py
	bin/buildout

test:
	mkdir -p tmp
	bin/py.test -x -v test/test.py --junitxml=tmp/testreport.xml


.PHONY: init test
