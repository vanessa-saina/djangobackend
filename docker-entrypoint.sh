#!/bin/bash

# install packages in the requirements.txt
pip install -r /application/requirements.txt

touch /application/logs/gunicorn.log
touch /application/logs/access.log
tail -n 0 -f /application/logs/*.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn insurance.wsgi:application \
    --bind 0.0.0.0:8003	 \
    --workers 5 \
    --log-level=info \
    --preload \
    --log-file=/application/logs/gunicorn.log \
    --access-logfile=/application/logs/access.log \
    "$@"