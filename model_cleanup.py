import os, sys

proj_path = os.path.realpath(__file__) 
print(proj_path)
p = os.path.dirname(proj_path)
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swarma.settings")
sys.path.append(p)

# This is so my local_settings.py gets loaded.
os.chdir(p)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from api.models import Node, Cluster

print(Node.objects.all())
print(Cluster.objects.all())
print(Node.objects.all().delete())
print(Cluster.objects.all().delete())
print(Node.objects.all())
print(Cluster.objects.all())
