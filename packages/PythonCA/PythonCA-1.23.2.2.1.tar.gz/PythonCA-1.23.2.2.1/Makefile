#!make
# -*- coding:utf-8 -*-
#
.PHONY: update_hgstamp
.phony:distclean checkin release cVXI11 build device_clear all clean readme install

all:clean cVXI11 vxi11scan vxi11_device_clear

CC=/usr/bin/clang
CXX=/usr/bin/clang++

# from https://www.mercurial-scm.org/wiki/VersioningWithMake
#HGVERSION:= $(shell hg parents --template 'hgid: {node|short}')
HGVERSION:= $(shell hg parents --template 'HGTagShort = \\\"{latesttag}.{latesttagdistance}\\\"')
HGVERSION_NO:= $(shell hg parents --template '{latesttag}.{latesttagdistance}')
VERSION:= $(shell python3 setup.py --version)

hgstamp.py: update_hgstamp
	[ -f $@ ] || touch $@
	echo $(HGVERSION) | cmp -s $@ - || echo $(HGVERSION) > $@
#

distclean:
	-rm ./build/bdist.*

checkin :
	-hg ci -m "before release $(HGVERSION_NO)"
	hg kwexpand
	make hgstamp.py

release: distclean
	make readme
	make hgstamp.py
	hg bookmark -i "release $(HGVERSION_NO)"
	python3 setup.py sdist

upload:
	python3 -m twine upload  dist/PythonCA-$(VERSION).tar.gz

	#python3 -m twine upload  dist/PyVXI11-$(shell hg parents --template '{latesttag}.{latesttagdistance}').tar.gz

pythonca: setup.py hgstamp.py
	python setup.py clean
	-python3 setup.py clean
	python setup.py build
	-python3 setup.py build

install:
	rm -r ./build/bdist.*
	python3 setup.py install
	rm -r ./build/bdist.*
	python2 setup.py install

build: pythonca


readme: README.rst
	/usr/local/bin/pandoc -t plain -o README.txt README.rst
	/usr/local/bin/pandoc -t html -o README.html README.rst
	/usr/local/bin/pandoc -t markdown -o README.md README.rst

sdist:
	python3 setup.py sdist

