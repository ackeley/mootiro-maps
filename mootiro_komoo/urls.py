#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default
from django.conf.urls.defaults import patterns, include, url


# Some URL fragments to be reused throughout the application
COMMUNITY_SLUG = r'(?P<community_slug>[a-zA-Z0-9-]+)'
NEED_SLUG = r'(?P<need_slug>[a-zA-Z0-9-]+)'


def prepare_regex(regex):
    return regex.replace('COMMUNITY_SLUG', COMMUNITY_SLUG).replace('NEED_SLUG', NEED_SLUG)


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # admin stuff
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # user and CAS urls
    url(r'^user/', include('user_cas.urls')),

    url(r'^tinymce/', include('tinymce.urls')),
    url(r'', include('need.urls')),
    url(r'', include('proposal.urls')),
    url(r'^comments/', include('komoo_comments.urls')),

    # Community URLs go last because one of them can match anything
    url(r'', include('community.urls')),
)