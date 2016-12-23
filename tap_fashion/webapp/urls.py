from django.conf.urls import url

from . import views

app_name = 'webapp'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^post/$', views.NewPostView.as_view(), name='post'),
    url(r'^post/newPost/', views.storePost, name='newPost'),
    url(r'^dashboard/storeComment/', views.storeComment, name='newComment'),
    url(r'^related/', views.RelatedPostsView.as_view(), name='related_posts'),
    url(r'^user/login/$', views.user_login, name='user_login'),
    url(r'^related/$', views.RelatedPostsView, name='related_posts'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^profilesearch/$', views.ProfilesearchView.as_view(), name='profilesearch'),

]
