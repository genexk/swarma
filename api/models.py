# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Cluster(models.Model):
    clustername = models.CharField(max_length=100, primary_key=True)
    meta = models.TextField(blank=True)
    datetime_added = models.DateTimeField(auto_now_add = True)
    datetime_modified = models.DateTimeField(auto_now = True) 
    join_token_manager = models.CharField(max_length=200, blank=True)
    join_token_worker = models.CharField(max_length=200, blank=True)
        
    def __str__(self):
        return 'Cluster: %s'%self.clustername


class Node(models.Model):
    hostname = models.CharField(max_length=100, primary_key=True)
    ip = models.GenericIPAddressField(protocol='IPv4', null=True,blank=True)
    cluster = models.ForeignKey(Cluster)


    MASTER = 'master'
    WORKER = 'worker'
    INACTIVE = 'inactive'
    ROLES_CHOICES = (
        (MASTER, 'master'),
        (WORKER, 'worker'),
        (INACTIVE, 'inactive'),
    )
    role = models.CharField(
        max_length=10,
        choices = ROLES_CHOICES,
        default=INACTIVE,
    )

    
    locked = models.BooleanField()
    meta = models.TextField(blank=True)
    datetime_added = models.DateTimeField(auto_now_add = True)
    datetime_modified = models.DateTimeField(auto_now = True)

    def __str__(self):
        return 'Node: %s'%self.hostname
