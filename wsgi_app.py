#!/usr/bin/env python
# coding: utf-8
# yc@2011/09/10

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'djblog.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
