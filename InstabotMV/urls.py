from django.conf.urls import url
from django.urls import path
from . import views
from InstabotMV.views import MediaList


app_name = 'instabot'

urlpatterns = [
    url('show/(?P<username_url>\w+)/$', views.ShowView.as_view(), name='show'),
    url('login/$', views.LoginView.as_view(), name='login'),
    url('logout/$', views.logout, name='logout'),
    url('dashboard/$', views.DashboardView, name='dashboard'),
    url('dashboard/$', views.tag_child, name='dashload'),
    url('hashtag_ajax/$', views.hashtags.as_view(), name='hashtags'),
    url('dashboard/task/new$', views.NewTask, name='newTask'),
    url('tags/(?P<id_tag>\d+)/$', views.tags, name='tags'),
    url('change/(?P<cred>\d+)/$', views.changeAccount, name='changeAccount'),
    url('dashboard/task/new/follow-like/$', views.NewFollowLike, name='newFollowLike'),
    url('dashboard/task/new/unfollow-task/$', views.UnfollowTask.as_view(), name='unfollow_task'),
    url('dashboard/accounts/$', views.UserAccounts.as_view(), name='userAccounts'),
    url('create/$', views.Create, name='create'),
    url('store-new-task/$', views.StoreTask.as_view(), name='storeTask'),
    url('store-new-task-u/$', views.StoreTaskUser.as_view(), name='storeTaskU'),
    url('delete_task/(?P<id_task>\d+)/$', views.DeleteTask,name="del_task"),

    # # ******************************** bot url's ************************************************************
    url('start-bot/$', views.StartBot.as_view(),name='start'),
    url('start/(?P<task>\d+)/$', views.start,name='starter'),
    url('stop-bot/$', views.StopBot.as_view(), name='stopBot'),
    url('imprimir/$', views.pruebaimpresion, name='impresion'),
    url('generate/$', views.GenerateRandomUserView.as_view(), name='generate')


]
