#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default
import json

from django import forms
from django.utils.translation import ugettext_lazy as _
from markitup.widgets import MarkItUpWidget
from fileupload.forms import FileuploadField
from fileupload.models import UploadedFile
from ajaxforms import AjaxModelForm
from annoying.functions import get_object_or_None

from main.utils import MooHelper
from main.widgets import TaggitWidget, ContactsWidget
from community.models import Community
from komoo_project.models import Project
from signatures.signals import notify_on_update
from video.forms import VideosField
from video.models import Video


class CommunityForm(AjaxModelForm):
    class Meta:
        model = Community
        fields = ('name', 'short_description', 'population', 'description',
                  'tags', 'contacts', 'geometry', 'files', 'videos',
                  'project_id')

    _field_labels = {
        'name': _('Name'),
        'short_description': _('Short description'),
        'population': _('Population'),
        'description': _('Description'),
        'contacts': _('Contacts'),
        'tags': _('Tags'),
        'files': ' ',
        'videos': _('Videos'),
    }

    description = forms.CharField(widget=MarkItUpWidget())
    geometry = forms.CharField(widget=forms.HiddenInput())
    files = FileuploadField(required=False)
    videos = VideosField(required=False)
    contacts = forms.CharField(required=False, widget=ContactsWidget())
    tags = forms.Field(
        widget=TaggitWidget(autocomplete_url="/community/search_tags/"),
        required=False)
    project_id = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *a, **kw):
        self.helper = MooHelper(form_id="community_form")
        return super(CommunityForm, self).__init__(*a, **kw)

    @notify_on_update
    def save(self, *args, **kwargs):
        comm = super(CommunityForm, self).save(*args, **kwargs)
        UploadedFile.bind_files(
            self.cleaned_data.get('files', '').split('|'), comm
        )

        videos = json.loads(self.cleaned_data.get('videos', ''))
        Video.save_videos(videos, comm)

        # Add the community to project if a project id was given.
        project_id = self.cleaned_data.get('project_id', None)
        if project_id:
            project = get_object_or_None(Project, pk=int(project_id))
            if project:
                project.save_related_object(comm, self.user)

        return comm
