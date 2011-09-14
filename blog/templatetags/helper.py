#!/usr/bin/env python
# coding: utf-8
# yc@2011/08/29

from blog.models import Post, Tag, Link, Page
from django import template

register = template.Library()

class CaptureasNode(template.Node):
	def __init__(self, nodelist, varname):
		self.nodelist = nodelist
		self.varname = varname

	def render(self, context):
		output = self.nodelist.render(context)
		context[self.varname] = output
		return ''

class AssignNode(template.Node):
	def __init__(self, name, value, need_resolve=True):
		self.name = name
		self.value = value
		self.need_resolve = need_resolve
		
	def render(self, context):
		context[self.name] = self.value.resolve(context, True) if self.need_resolve else self.value
		return ''

# captureas tag, from: http://djangosnippets.org/snippets/545/
@register.tag(name='captureas')
def do_captureas(parser, token):
	try:
		tag_name, args = token.contents.split(None, 1)
	except ValueError:
		raise template.TemplateSyntaxError("'captureas' node requires a variable name.")
	nodelist = parser.parse(('endcaptureas',))
	parser.delete_first_token()
	return CaptureasNode(nodelist, args)

# assign tag, from: http://djangosnippets.org/snippets/539/
@register.tag(name='assign')
def do_assign(parser, token):
	"""
	Assign an expression to a variable in the current context.
	
	Syntax::
		{% assign [name] [value] %}
	Example::
		{% assign list entry.get_related %}
		
	"""
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
	value = parser.compile_filter(bits[2])
	return AssignNode(bits[1], value)

@register.tag(name='getnavas')
def get_nav(parser, token):
	"""	获取导航栏（单页面列表）：{% getnavas navs  %}"""
	try:
		tag, var = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

	return AssignNode(var, [Page(**i) for i in Page.objects.values('id', 'title', 'slug' )], need_resolve=False)

@register.inclusion_tag('sidebar/recent_posts.html')
def get_recent_posts(num):
	return {'recent_posts': Post.objects.recent(int(num))}

@register.inclusion_tag('sidebar/top_tags.html')
def get_top_tags(num):
	return {'top_tags': Tag.objects.top(int(num))}

@register.inclusion_tag('sidebar/links.html')
def get_links(num):
	return {'links': Link.objects.all()[:int(num)]}
