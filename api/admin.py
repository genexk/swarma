# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Node, Cluster
admin.site.register(Cluster)
admin.site.register(Node)
