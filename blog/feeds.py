#!/usr/bin/env python
# coding: utf-8
# yc@2011/08/31

from models import Post
from django.conf import settings
from django.contrib.syndication.views import Feed

class LatestPostFeed(Feed):
	title = settings.SITE_TITLE
	link = 'feed'
	description  = settings.SITE_DESC

	def items(self):
		return Post.objects.all()[:settings.RECENT_COUNT]

	def item_title(self, item):
		return item.title

	def item_description(self, item):
		return item.content
