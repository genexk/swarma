from django.conf.urls import url


from . import views


urlpatterns = [
    url(r'cluster',views.get_cluster_info),
    url(r'$^', views.index, name='index'),
]

