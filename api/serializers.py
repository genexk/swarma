from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Node

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class NodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Node 
        fields = ('hostname', 'ip', 'cluster', 'role', 'locked')
