# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.contrib.contenttypes import generic
from django.template.defaultfilters import slugify
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from lib.taggit.managers import TaggableManager

from main.mixins import BaseModel
from main.models import ContactsField
from authentication.models import User
from community.models import Community
from komoo_map.models import GeoRefModel, POLYGON, LINESTRING, POINT
from fileupload.models import UploadedFile
from search.signals import index_object_for_search


class ResourceKind(models.Model):
    """Kind of Resources"""
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(ResourceKind, self).save(*args, **kwargs)

    @classmethod
    def favorites(cls, number=10):
        return ResourceKind.objects.all().exclude(name='').annotate(
            count=Count('resource__id')).order_by('-count', 'slug')[:number]


class Resource(GeoRefModel, BaseModel):
    """Resources model"""
    name = models.CharField(max_length=256, default=_('Resource without name'))
    # slug = models.CharField(max_length=256, blank=False, db_index=True)
    kind = models.ForeignKey(ResourceKind, null=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=250, null=True, blank=True)
    contacts = ContactsField()
    tags = TaggableManager()

    community = models.ManyToManyField(Community, related_name='resources',
            null=True, blank=True)  # TODO remove me

    # Meta info
    creator = models.ForeignKey(User, editable=False, null=True,
                                related_name='created_resources')
    creation_date = models.DateTimeField(auto_now_add=True)
    last_editor = models.ForeignKey(User, editable=False, null=True,
                                    blank=True)
    last_update = models.DateTimeField(auto_now=True)

    class Map:
        title = _('Resource')
        editable = True
        background_color = '#28CB05'
        border_color = '#1D9104'
        geometries = (POLYGON, LINESTRING, POINT)
        form_view_name = 'new_resource_from_map'
        zindex = 15

    def __unicode__(self):
        return unicode(self.name)

    image = "img/resource.png"
    image_off = "img/resource-off.png"
    default_logo_url = "img/logo-resource.png"

    def files_set(self):
        """ pseudo-reverse query for retrieving Resource Files"""
        return UploadedFile.get_files_for(self)

    @property
    def home_url_params(self):
        return dict(id=self.id)

    @property
    def view_url(self):
        return reverse('view_resource', kwargs=self.home_url_params)

    @property
    def edit_url(self):
        return reverse('edit_resource', kwargs=self.home_url_params)

    @property
    def admin_url(self):
        return reverse('admin:{}_{}_change'.format(self._meta.app_label,
            self._meta.module_name), args=[self.id])

    @property
    def perm_id(self):
        return 'r%d' % self.id

    def save(self, *args, **kwargs):
        r_ = super(Resource, self).save(*args, **kwargs)
        index_object_for_search.send(sender=self, obj=self)
        return r_

    # ==========================================================================
    # Utils

    # def from_dict(self, data):
    #     keys = ['id', 'name', 'contact', 'geojson',  'creation_date',
    #             'is_admin', 'is_active', 'about_me']
    #     date_keys = ['creation_date']
    #     build_obj_from_dict(self, data, keys, date_keys)

    def to_dict(self):
        fields_and_defaults = [
            ('name', None), ('kind_id', None), ('description', None),
            ('short_description ', None),
            ('creator_id', None), ('creation_date', None),
            ('last_editor_id', None), ('last_update', None),
            ('geojson', {}), ('contacts', {}),
        ]
        dict_ = {v[0]: getattr(self, v[0], v[1]) for v in fields_and_defaults}
        dict_['tags'] = [tag.name for tag in self.tags.all()]
        return dict_

    # def is_valid(self, ignore=[]):
    #     self.errors = {}
    #     valid = True
    #     return valid
