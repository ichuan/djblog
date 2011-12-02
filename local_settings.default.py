#!/usr/bin/env python
# coding: utf-8
# yc@2011/08/26

import os

# 时区
TIME_ZONE = 'Asia/Shanghai'

# 语言
LANGUAGE_CODE = 'zh-cn'

# 邮箱（报错时发送）
EMAIL = 'iyanchuan@gmail.com'

# 数据库信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # mysql 可以改成 'postgresql_psycopg2', 'postgresql', 'sqlite3' or 'oracle'.
        'NAME': 'djblog',                      # 数据库名
        'USER': 'root',                      # sqlite3 不使用此配置
        'PASSWORD': 'root',                  # sqlite3 不使用此配置
        'HOST': '',
        'PORT': '',
    }
}

# 主题
THEME = 'classic'

# 站点名称
SITE_TITLE = 'ichuan.net'
# 副标题
SITE_SUBTITLE = u'All about yc'
# 作者
SITE_AUTHOR = 'yc'
# 描述
SITE_DESC = 'yc\'s personal site'

# 分页大小
PER_PAGE = 5
# recent 个数
RECENT_COUNT = 5

# google 统计的 id
GA_ID = 'UA-15372596-1'

# google custom search id, see http://www.google.com/cse/
CSE_ID = '017823656936221718810:8oexw_fkbz0'

# disqus 评论 id
DISQUS_SHORTNAME = 'ycsblog'


#### 以下配置不要改动 ####
TEMPLATE_DIRS = (
	os.path.join(os.path.dirname(__file__), 'templates/' + THEME),
)
ADMINS = (
    ('admin', EMAIL),
)
MANAGERS = ADMINS
