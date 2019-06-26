from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^dashboard$', views.dashboard),
    url(r'^new$', views.new_wish),
    url(r'^granted', views.granted),
    url(r'^edit$', views.edit),
    url(r'^logout$', views.logout),
    url(r'^delete$', views.delete),
    url(r'^process$', views.process_edit),
    url(r'^like$', views.like_wish),
    url(r'^stats', views.stats)
]