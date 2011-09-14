#!/bin/sh

uwsgi -s /tmp/uwsgi.sock -C -M -p 4 -t 30 --limit-as 128 -R 10000 --vhost -d /tmp/uwsgi.log --pidfile /tmp/uwsgi.pid --pythonpath /var/www
