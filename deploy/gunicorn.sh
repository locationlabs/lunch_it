#!/bin/bash

set -e

LOGFILE=/var/log/gunicorn/lunchit.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
USE_USER=www-data
USE_GROUP=www-data

cd /var/wsgi/lunch_it/lunch_it
source ../env/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR

nohup ../env/bin/gunicorn_django -w $NUM_WORKERS \
    --user=$USE_USER --group=$USE_GROUP --log-level=debug \
    --pythonpath=/var/wsgi/lunch_it/lunch_it --settings=lunch_it.settings \
    --log-file=$LOGFILE 2>>$LOGFILE &

