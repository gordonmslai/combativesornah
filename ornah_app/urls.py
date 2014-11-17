from django.conf.urls import patterns, include, url
from django.contrib import admin
from scrape import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ornah_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.loading, name='loading'),
    url(r'^index/$', views.index, name='index_s'),
    url(r'^index/(-?[0-9]*)/$', views.index, name='index_s'),
    url(r'^index2/', views.index2, name='index2'),

)
