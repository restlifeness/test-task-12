#!/bin/bash

alembic upgrade head

python3 src/main.py 
