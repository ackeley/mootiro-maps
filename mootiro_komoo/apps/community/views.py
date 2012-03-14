#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import json
import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Polygon
from django.db.models.query_utils import Q

from annoying.decorators import render_to

from community.models import Community
from community.forms import CommunityForm, CommunityMapForm
from main.utils import create_geojson

logger = logging.getLogger(__name__)


@login_required
def edit(request, community_slug=""):
    logger.debug('acessing Community > edit')

    if request.is_ajax():
        template = "community/edit_ajax.html"
    else:
        template = "community/edit.html"

    if community_slug:
        community = get_object_or_404(Community, slug=community_slug)
    else:
        community = Community(creator=request.user)

    if request.POST:
        form = CommunityForm(request.POST, instance=community)
        if form.is_valid():
            community = form.save()
            community.save()

            if not request.is_ajax():
                return redirect(view, community.slug)

            rdict = dict(redirect=reverse('view_community',
                                    args=(community.slug,)))
        else:
            rdict = dict(form=form, community=community)
    else:
        form = CommunityForm(instance=community)
        rdict = dict(form=form, community=community)
    return render(request, template, rdict)


@render_to('community/on_map.html')
def on_map(request, community_slug):
    logger.debug('acessing Community > on_map : community_slug={}'.format(
            community_slug))

    community = get_object_or_404(Community, slug=community_slug)
    geojson = create_geojson([community])
    mapform = CommunityMapForm({'map': geojson})
    return dict(community=community, form=mapform)


@render_to('community/view.html')
def view(request, community_slug):
    logger.debug('acessing Community > view : community_slug={}'.format(
            community_slug))

    community = get_object_or_404(Community, slug=community_slug)
    geojson = create_geojson([community])
    return dict(community=community, geojson=geojson)


@render_to('community/map.html')
def map(request):
    logger.debug('acessing Community > map')
    form = CommunityMapForm(request.POST)
    return dict(form=form)


def communities_geojson(request):
    bounds = request.GET.get('bounds', None)
    x1, y2, x2, y1 = [float(i) for i in bounds.split(',')]
    polygon = Polygon(((x1, y1), (x1, y2), (x2, y2), (x2, y1), (x1, y1)))
    communities = Community.objects.filter(geometry__intersects=polygon)
    geojson = create_geojson(communities)
    return HttpResponse(json.dumps(geojson),
        mimetype="application/x-javascript")


def search_by_name(request):
    logger.debug('acessing Community > search_by_name')
    term = request.GET['term']
    # rx = "^{0}|\s{0}".format(term)  # matches only beginning of words
    # communities = Community.objects.filter(Q(name__iregex=rx) | Q(slug__iregex=rx))
    communities = Community.objects.filter(Q(name__icontains=term) |
                                           Q(slug__icontains=term))
    d = [{'value': c.id, 'label': c.name} for c in communities]
    return HttpResponse(simplejson.dumps(d), mimetype="application/x-javascript")
