#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import json
import logging

from django.shortcuts import get_object_or_404, redirect
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


@render_to('community/community_edit.html')
@login_required
def edit(request, community_slug=""):
    logger.debug('acessing Community > edit')

    if community_slug:
        community = get_object_or_404(Community, slug=community_slug)
        action = reverse('edit_community', args=(community_slug,))
    else:
        community = None
        action = reverse('new_community')
    if request.POST:
        POST = request.POST.copy()
        POST['geometry'] = json.dumps(
                json.loads(POST['geometry'])['geometries'][0])
        form = CommunityForm(POST, instance=community)
        if form.is_valid():
            community = form.save(commit=False)
            if community.id:  # was never saved
                community.creator = request.user
            community.save()

            if not request.is_ajax():
                return redirect(view, community.slug)

            return {'redirect': reverse('view_community',
                                        args=(community.slug,))}
        else:
            return dict(form=form, action=action, community=community)
    else:
        return dict(form=CommunityForm(instance=community), action=action,
                    community=community)


@render_to('community/community_view.html')
def view(request, community_slug):
    logger.debug('acessing Community > view : community_slug={}'.format(
            community_slug))

    community = get_object_or_404(Community, slug=community_slug)
    geojson = create_geojson([community])
    mapform = CommunityMapForm({'map': geojson})
    return dict(community=community, form=mapform)


@render_to('community/community_map.html')
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
    return HttpResponse(simplejson.dumps(d),
        mimetype="application/x-javascript")
