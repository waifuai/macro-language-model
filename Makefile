# Makefile for the project

.PHONY: all run test clean

all: run

run:
	python main.py

test:
	python -m unittest discover tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete