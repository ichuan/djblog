# coding: utf-8
# author: yc@/2011/8/26

import markdown
from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

class TagManager(models.Manager):
	def recount(self, *args, **kwargs):
		'''重新统计每个tag对应的文章数，删除空标签'''
		for i in self.filter(*args, **kwargs):
			i.count_post = i.post_set.count()
			if i.count_post <= 0:
				i.delete()
			else:
				i.save()

	def decr_count(self, ids, delete_isolate=True):
		'''文章数减1'''
		assert all(map(lambda i:isinstance(i, (int, long)), ids))
		self.extra(where=['id in (%s)' % ','.join(map(str, ids))]).update(count_post=F('count_post') - 1)
		if delete_isolate:
			# 删除没有和文章关联的标签
			self.filter(count_post__lte=0).delete()

	def incr_count(self, ids):
		'''文章数减1'''
		assert all(map(lambda i:isinstance(i, (int, long)), ids))
		self.extra(where=['id in (%s)' % ','.join(map(str, ids))]).update(count_post=F('count_post') + 1)

	def top(self, num):
		return self.order_by('-count_post')[:num]

class Tag(models.Model):
	'''标签'''
	name = models.CharField(max_length=200, unique=True, verbose_name=u'名称')
	count_post = models.IntegerField(default=0, editable=False, verbose_name=u'文章数')
	objects = TagManager()

	def __unicode__(self):
		return u'%s (%d)' % (self.name, self.count_post)

	def get_absolute_url(self):
		return u'/tag/%s/' % self.name

	class Meta:
		verbose_name_plural = verbose_name = u'标签'

class Page(models.Model):
	'''单页'''
	title = models.CharField(max_length=200, verbose_name=u'标题')
	slug = models.CharField(max_length=50, unique=True, db_index=True, verbose_name=u'Slug', help_text=u'页面的 URL 名称。可包含字母、数字、减号、下划线，不能是以下词语之一：archives、post、tag')
	author = models.ForeignKey(User, editable=False)
	markdown = models.TextField(verbose_name=u'内容')
	content = models.TextField(blank=True, editable=False)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'发布日期')
	allow_comment = models.BooleanField(default=False, verbose_name=u'允许评论')
	seq = models.IntegerField(default=0, db_index=True, verbose_name=u'排序')
	
	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return u'/%s/' % self.slug
	get_absolute_url.short_description = u'URL'

	class Meta:
		ordering = ['seq']
		verbose_name_plural = verbose_name = u'页面'

class PostManager(models.Manager):
	def recent(self, num, quick=True):
		'''获取最近的num条文章'''
		if quick:
			return [Post(**i) for i in Post.objects.values('id', 'title', 'slug')[:num]]
		return Post.objects.all()[:num]
		

class Post(models.Model):
	'''文章'''
	title = models.CharField(max_length=200, verbose_name=u'标题')
	slug = models.CharField(max_length=50, blank=True, verbose_name=u'Slug', help_text=u'本文的短标签，将出现在文章 URL 中。可包含字母、数字、减号、下划线，如：does-python-optimize-function-calls-from-loops')
	author = models.ForeignKey(User, editable=False)
	markdown = models.TextField(verbose_name=u'内容')
	content = models.TextField(blank=True, editable=False)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'发布日期')
	count_hit = models.IntegerField(default=0, editable=False, verbose_name=u'点击数')
	tags = models.ManyToManyField(Tag, blank=True, verbose_name=u'标签')
	objects = PostManager()

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return u'/post/%d/%s/' % (self.id, self.slug or self.title.replace('/', '-'))

	class Meta:
		get_latest_by = 'created_at'
		ordering = ['-id']
		verbose_name_plural = verbose_name = u'文章'

class Link(models.Model):
	'''链接'''
	name = models.CharField(max_length=200, verbose_name=u'名称')
	url = models.URLField(verify_exists=False, verbose_name=u'链接')
	seq = models.IntegerField(default=0, db_index=True, verbose_name=u'排序')

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['seq']
		verbose_name_plural = verbose_name = u'链接'
