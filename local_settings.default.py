#!/usr/bin/env python
# coding: utf-8
# yc@2011/08/26

import os

################################### 
# 用户设置
################################### 

# 站点名称
SITE_TITLE = 'djblog'

# 副标题
SITE_SUBTITLE = u'djblog'

# 作者
SITE_AUTHOR = 'TY'

# 域名
DOMAIN = 'http://t-y.me'

# 新浪微博
WEIBO = 'http://weibo.com/tyminiblog2010'

# 豆瓣主页
DOUBAN = 'http://www.douban.com/people/T-y/'

# 描述
SITE_DESC = 'a new blog powerd by djblog'

# 主题
THEME = 'douban'
#THEME = 'classic'

# google 统计的 id
GA_ID = 'UA-15372596-1'

# google custom search id, see http://www.google.com/cse/
CSE_ID = '017823656936221718810:8oexw_fkbz0'

# disqus 评论 id
DISQUS_SHORTNAME = 'ycsblog'


################################### 
# 全局设置
################################### 

# 数据库信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # mysql 可以改成 'postgresql_psycopg2', 'postgresql', 'sqlite3' or 'oracle'.
        'NAME': 'test',                      # 数据库名
        'USER': 'root',                      # sqlite3 不使用此配置
        'PASSWORD': '',                  # sqlite3 不使用此配置
        'HOST': '',
        'PORT': '',
    }
}

# 时区
TIME_ZONE = 'Asia/Shanghai'

# 语言
LANGUAGE_CODE = 'zh-cn'

# 邮箱（报错时发送）
EMAIL = 'admin@gmail.com'


# 分页大小
PER_PAGE = 5

# recent 个数
RECENT_COUNT = 5

#### 以下配置不要改动 ####
TEMPLATE_DIRS = (
	os.path.join(os.path.dirname(__file__), 'templates/' + THEME),
)
ADMINS = (
    ('admin', EMAIL),
)
MANAGERS = ADMINS
