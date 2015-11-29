from django.conf.urls import patterns, url
from django.views.generic import TemplateView
import views


urlpatterns = patterns('geonode.odk.views',
   url(r'^$', views.odk_tables_list, name="odk_list"),
   url(r'^settings$', views.odk_settings, name="odk_settings"),
)