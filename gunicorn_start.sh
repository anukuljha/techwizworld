#!/bin/bash

NAME="billing"                                  # Name of the application
DJANGODIR=/home/ubuntu/billing             # Django project directory
#SOCKFILE=/webapps/hello_django/run/gunicorn.sock  # we will communicte using this unix socket
USER=ubuntu                                        # the user to run as                                     # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=studyabacus_accounts.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=studyabacus_accounts.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
#export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn studyabacus_accounts.wsgi
