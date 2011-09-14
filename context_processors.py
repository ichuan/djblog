#!/usr/bin/env python
# coding: utf-8
# yc@2011/08/27

from django.conf import settings

def consts(request):
	ret = {}
	for i in ('SITE_TITLE', 'SITE_SUBTITLE', 'SITE_AUTHOR', 'SITE_DESC', 'DISQUS_SHORTNAME', 'GA_ID', 'CSE_ID'):
		ret[i] = getattr(settings, i)
	return ret
