#! /usr/bin/env python
# -*- coding:utf-8 -*-

from fabric.state import env
from fabric.api import task, execute

from .base import virtualenv


@task
def elasticsearch():
    """ download and place elastic search on the lib folder """
    # FIXME: Hard coded version is evil.
    with virtualenv():
        env.run(''
                'wget -P lib/ http://download.elasticsearch.org/elasticsearch/'
                'elasticsearch/elasticsearch-0.20.5.tar.gz;'
                'tar xzvf lib/elasticsearch-0.20.5.tar.gz -C lib/;'
                'mv lib/elasticsearch-0.20.5 lib/elasticsearch;'
                'rm lib/elasticsearch-0.20.5.tar.gz;'
                )


@task(default=True)
def all():
    execute('install.requirements')
    execute('install.patch')
    execute('install.elasticsearch')


@task(aliases=['develop', 'development'])
def dev():
    execute('install.all')


@task(alias='django_patch')
def patch():
    """
    build env_ironment: pip install everything + patch django for postgis
    encoding problem on postgres 9.1
    """
    with virtualenv():
        env.run("patch -p0 `which python | "
                "sed -e 's/bin\/python$/lib\/python2.7\/site-packages\/django\/"
                "contrib\/gis\/db\/backends\/postgis\/adapter.py/'` "
                "../docs/postgis-adapter-2.patch")

@task
def requirements():
    with virtualenv(), env.cd('mootiro_maps'):
        env.run('pip install -r settings/requirements.txt')
