# coding:utf-8

import imghdr, time, os
from django.http import Http404, HttpResponse
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

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

@login_required
def upload_image(request):
	'''上传图片'''
	if request.method != 'POST':
		raise Http404
	path = 'null'
	msg = ''
	if 'image' in request.FILES:
		f = request.FILES['image']
		if f.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
			msg = 'alert("Image size too large!");'
		else:
			ext = imghdr.what(f.file)
			if not ext:
				msg = 'alert("Not an image file!");'
			else:
				path = 'static/upload/%d.%s' % (int(time.time() * 1000), ext)
				os_path = os.path.join(settings.ROOT_DIR, path)
				path = '"/%s"' % path
				open(os_path, 'wb+').write(f.read())
	else:
		msg = 'alert("No image file selected!");'
	return HttpResponse('<script>%s;top._image_callback_(%s)</script>'
						% (msg, path))
