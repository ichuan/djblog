#!/usr/bin/env python
# coding: utf-8
# yc@2011/09/02

'''
Backup files to your dropbox account
i.e. python dropback.py -k abc -s def -u i@u.com -p mypasswd -f /tmp/a.zip -t /backup/
'''
import sys
from optparse import OptionParser
from dropbox import client, auth

class DropBack(object):
	''''''
	def cp(self, local, remote_path):
		'''把一个文件保存到dropbox服务器上'''
		obj = open(local, 'rb')
		try:
			return self.client.put_file('dropbox', remote_path, obj)
		finally:
			obj.close()

	def login(self, options):
		'''获得access token'''
		config = {
			'server': 'api.dropbox.com',
			'content_server': 'api-content.dropbox.com',
			'port': 80,
			'request_token_url': 'https://api.dropbox.com/0/oauth/request_token',
			'access_token_url': 'https://api.dropbox.com/0/oauth/access_token',
			'authorization_url': 'https://www.dropbox.com/0/oauth/authorize',
			'trusted_access_token_url': 'https://api.dropbox.com/0/token',
			'consumer_key': options['key'],
			'consumer_secret':options['secret'],
		}
		dba = auth.Authenticator(config)
		token = dba.obtain_request_token()
		self.access_token = dba.obtain_trusted_access_token(options['email'], options['passwd'])
		self.client = client.DropboxClient(config['server'], config['content_server'], config['port'], dba, self.access_token)

	def main(self):
		'''解析命令行参数，执行备份'''
		parser = OptionParser(usage='e.g. %prog -k abc -s def -u i@u.com -p mypasswd -f /tmp/a.zip -t /backup/')
		parser.add_option('-k', '--key', help='Dropbox App key', dest='consumer_key')
		parser.add_option('-s', '--secret', help='Dropbox App secret', dest='consumer_secret')
		parser.add_option('-f', '--file', help='File to backup', dest='local')
		parser.add_option('-t', '--to', help='Remote path to save', dest='remote_path')
		parser.add_option('-u', '--user', help='Your Dropbox account', dest='email')
		parser.add_option('-p', '--passwd', help='Your Dropbox password', dest='passwd')
		options, args = parser.parse_args()

		if not options.consumer_key or not options.consumer_secret:
			parser.error('key and secret must be set')
		if not options.local or not options.remote_path:
			parser.error('missing local file or remote path')
		if not options.email or not options.passwd:
			parser.error('missing account and password')

		try:
			self.login(dict(key=options.consumer_key, secret=options.consumer_secret,\
						email=options.email, passwd=options.passwd))
		except Exception, e:
			print 'Obtaining access token error: ' + str(e)
			sys.exit(-1)

		try:
			self.cp(options.local, options.remote_path)
		except Exception, e:
			print 'Puting files error: ' + str(e)
			sys.exit(-1)

a = DropBack()
a.main()
