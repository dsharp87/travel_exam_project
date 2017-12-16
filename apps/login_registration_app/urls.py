from django.conf.urls import url
from . import views 

print "im in apps urls"

#login_registration_app file
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^travels$', views.travels),
    url(r'^travels/add_trip_form$', views.add_trip_form),
    url(r'^travels/process_new_trip$', views.process_new_trip),
    url(r'^travels/show_trip/(?P<trip_id>\d+)$', views.show_trip),
    url(r'^travels/join_trip/(?P<trip_id>\d+)$', views.join_this_trip),
]