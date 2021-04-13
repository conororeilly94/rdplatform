from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^posts/(?P<word>.*)/$', views.posts_detail, name='posts_detail'),
    url(r'^panel/posts/list/$', views.posts_list, name='posts_list'),
    url(r'^panel/posts/add/$', views.posts_add, name='posts_add'),
    url(r'^panel/posts/del/(?P<pk>\d+)$', views.posts_delete, name='posts_delete'),
    url(r'^panel/posts/edit/(?P<pk>\d+)$', views.posts_edit, name='posts_edit'),
    url(r'^panel/posts/publish/(?P<pk>\d+)$', views.posts_publish, name='posts_publish'),
    url(r'^urls/(?P<pk>\d+)$', views.posts_detail_short, name='posts_detail_short'),
    url(r'^all/posts/(?P<word>.*)/$', views.posts_all_show, name='posts_all_show'),
    url(r'^all/posts/$', views.all_posts, name='all_posts'),
    url(r'^search/$', views.all_posts_search, name='all_posts_search'),
]