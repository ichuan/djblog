#!/usr/bin/env python
# coding: utf-8
# yc@2011/08/27

import markdown, re
from django import forms
from django.db.models import F
from django.contrib import admin
from models import Tag, Post, Link, Page

class TagAdmin(admin.ModelAdmin):
	list_display = ['name', 'count_post']

class LinkAdmin(admin.ModelAdmin):
	list_display = ['name', 'url']

class PageAdminForm(forms.ModelForm):
	class Meta:
		model = Page

	def clean_slug(self):
		slug = self.cleaned_data['slug']
		if re.match(r'^[a-z0-9A-Z_\-]+$', slug):
			return slug.strip()

		raise forms.ValidationError(u'slug 格式不正确')

class PageAdmin(admin.ModelAdmin):
	list_display = ['title', 'get_absolute_url', 'author', 'created_at', 'seq']
	form = PageAdminForm

	def save_model(self, request, obj, form, change):
		'''新建/编辑 页面'''
		obj.author = request.user
		obj.content = markdown.markdown(obj.markdown)

		return super(PageAdmin, self).save_model(request, obj, form, change)

class PostAdminForm(forms.ModelForm):
	class Meta:
		model = Post

	def clean_slug(self):
		slug = self.cleaned_data['slug']
		if not slug or re.match(r'^[a-z0-9A-Z_\-]+$', slug):
			return slug.strip()

		raise forms.ValidationError(u'slug 格式不正确')

class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'author', 'created_at', 'count_hit']
	list_filter = ['author', 'tags']
	form = PostAdminForm

	def save_model(self, request, obj, form, change):
		'''新建/编辑 文章'''
		is_editing = bool(obj.id)
		obj.author = request.user
		obj.content = markdown.markdown(obj.markdown)
		old_tags = None

		# 保存原有标签
		if is_editing:
			old_tags = set(Post.objects.get(id=obj.id).tags.values_list('id', flat=True))

		# 因为要在保存post和tag的关系之后处理tag计数，所以hook掉form的save_m2m
		_save_m2m = form.save_m2m
		def after_save():
			_save_m2m()
			if is_editing:
				new_tags = set(obj.tags.values_list('id', flat=True))
				# 得到需要增减计数的标签列表
				decr_tags = old_tags - new_tags
				incr_tags = new_tags - old_tags
				if incr_tags:
					Tag.objects.incr_count(incr_tags)
				if decr_tags:
					Tag.objects.decr_count(decr_tags)
			else:
				# 新文章，直接更新tags计数
				obj.tags.all().update(count_post=F('count_post') + 1)
		form.save_m2m = after_save
			
		return super(PostAdmin, self).save_model(request, obj, form, change)

	def delete_model(self, request, obj):
		'''删除文章'''
		tags = obj.tags.values_list('id', flat=True)
		# 减少标签计数
		if tags:
			Tag.objects.decr_count(tags)
		ret = super(PostAdmin, self).delete_model(request, obj)

admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Link, LinkAdmin)
