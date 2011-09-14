# coding:utf-8

from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

import utils
from models import Post

def show_post(request, pid):
	'''查看'''
	try:
		post = Post.objects.select_related().get(id=int(pid))
	except:
		raise Http404

	post.count_hit += 1
	post.save()
	tags = post.tags.all()

	return render_to_response('page.html', {
		'page': post,
		'footer': True,
		'sharing': True,
		'comments': True,
		'tags': tags,
		'keywords': ','.join([i.name for i in tags]),
	}, context_instance=RequestContext(request))

def list_by_tag(request, name):
	'''按标签'''
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1

	return render_to_response('index.html', {
		'title': name + ' - Tag',
		'posts': utils.get_page(Post.objects.filter(tags__name=name), page),
	}, context_instance=RequestContext(request))
