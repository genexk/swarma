from django.conf.urls import url


from . import views


urlpatterns = [
    url(r'^clusters',views.clusters),
    url(r'^nodes',views.nodes),
    url(r'^cluster',views.cluster),
    url(r'^node',views.node),
    url(r'^create_cluster', views.create_cluster),
    url(r'destroy', views.destroy_cluster),
    url(r'dashboard', views.dashboard),
    url(r'$^', views.index, name='index'),
]

