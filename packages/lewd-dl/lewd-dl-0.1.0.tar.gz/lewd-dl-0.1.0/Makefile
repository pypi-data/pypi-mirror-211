# Makefile for lewd-dl

EXT = $(wildcard lewd_dl/*/__pycache__) $(wildcard */__pycache__)
TARGET = bdist_wheel

all: clean build

clean:
	$(RM) -rf dist build lewd_dl.egg-info $(EXT)

build:
	python setup.py $(TARGET)

install: clean build
	pip install -e .

pypi-publish:
	python setup.py bdist_wheel sdist
	python -m twine check dist/*
	python -m twine upload -r pypi dist/*

.PHONY: all clean build install pypi-publish