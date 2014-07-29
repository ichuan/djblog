# coding:utf-8
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from blog.feeds import LatestPostFeed
from blog.models import Post, Page
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler404 = 'views.handler404'

sitemaps = {
	'blog': GenericSitemap({'queryset': Post.objects.all(), 'date_field': 'created_at'}),
	'page': GenericSitemap({'queryset': Page.objects.all(), 'date_field': 'created_at'}),
}

urlpatterns = patterns('',
    (r'^$', 'views.home'),
	(r'^archives/$', 'views.archives'),
    (r'^admin/', include(admin.site.urls)),
	(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}), # TODO 用nginx配置代替
)

# blogs
urlpatterns += patterns('blog.views',
	(r'^post/(?P<pid>\d+)/', 'show_post'),
	(r'^tag/(?P<name>.+)/$', 'list_by_tag'),
    (r'^feed/$', LatestPostFeed()),
	(r'^upload-image/', 'upload_image'),
)
