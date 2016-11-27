from django.conf.urls import url

from . import views

urlpatterns =[
#    url(r'^search', views.search, name='search'),
    url(r'^ViewPatterns/(?P<pk>[0-9]+)$', views.viewpatterns, name='viewpatterns'),
    url(r'^ShowPattern/(?P<pk>[0-9]+)$', views.showpattern, name='showpattern'),
    url(r'^$', views.index, name='index'),
]