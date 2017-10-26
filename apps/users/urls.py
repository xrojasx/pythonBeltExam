from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travel$', views.travel),
    url(r'^addtrip$', views.addtrip),
    url(r'^createtrip$', views.createtrip),
    url(r'^show/(?P<trip_id>\d+)$', views.show),
    url(r'^join/(?P<trip_id>\d+)$', views.join),
    url(r'^logout$', views.logout),
    url(r'^delete/(?P<id>\d+)$', views.delete)
]