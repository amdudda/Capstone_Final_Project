from django.conf.urls import url

from . import views

urlpatterns =[
#    url(r'^search', views.search, name='search'),
    url(r'^GeneratePattern/(?P<pk>[0-9]+)$', views.genpattern, name='genpatterns'),
    url(r'^ViewPatterns/(?P<pk>[0-9]+)$', views.viewpatterns, name='viewpatterns'),
    url(r'^ShowPattern/(?P<pk>[0-9]+)$', views.showpattern, name='showpattern'),
    url(r'^UploadImage', views.upload_image, name='uploadimage'),
    url(r'^Tag/(?P<tag>[A-Za-z0-9 ]+)', views.show_by_tag, name='tagged'),
    url(r'^About', views.about, name='about'),
    url(r'^$', views.index, name='index'),
]