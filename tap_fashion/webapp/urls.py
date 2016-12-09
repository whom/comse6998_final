from django.conf.urls import url

from . import views

app_name = 'webapp'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^post/$', views.NewPostView.as_view(), name='post'),
    url(r'^post/newPost/', views.storePost, name='newPost'),
    url(r'^dashboard/storeComment/', views.storeComment, name='newComment'),
]
