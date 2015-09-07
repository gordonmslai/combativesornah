from django.conf.urls import patterns, include, url
from django.contrib import admin
from scrape import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ornah_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^(-?[0-9]*)/$', views.index, name='index_s'),
)
