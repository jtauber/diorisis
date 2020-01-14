#!/bin/sh

isort scripts/*.py
black scripts/*.py
flake8 scripts/*.py
