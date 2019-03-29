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
    url('newaccount/$', views.NewAccount, name='addaccount'),
    url('dashboard/$', views.tag_child, name='dashload'),
    url('reports/$', views.report, name='report'),
    url('ajax/ticker/$', views.ticker, name='counter'),
    url('ajax/validate_username/$', views.test, name='test2'),
    url('hashtag_ajax/$', views.hashtags.as_view(), name='hashtags'),
    url('prueba_ajax/$', views.prueba.as_view(), name='prueba'),
    url('dashboard/task/new$', views.NewTask, name='newTask'),
    url('tags/(?P<id_tag>\d+)/$', views.tags, name='tags'),
    url('change/(?P<cred>\d+)/$', views.changeAccount, name='changeAccount'),
    url('dashboard/task/new/follow-like/$', views.NewFollowLike, name='newFollowLike'),
    url('dashboard/task/new/unfollow-task/$', views.UnfollowTask, name='unfollow_task'),
    url('dashboard/accounts/$', views.UserAccounts.as_view(), name='userAccounts'),
    url('dashboard/delaccount/(?P<id_cred>\d+)/$$', views.DeleteAccount, name='delaccount'),
    url('create/$', views.Create, name='create'),
    url('store-new-task/$', views.StoreTask.as_view(), name='storeTask'),
    url('store-new-task-u/$', views.StoreTaskUser.as_view(), name='storeTaskU'),
    url('delete_task/(?P<id_task>\d+)/$', views.DeleteTask,name="del_task"),
    url('edit_task/(?P<id_task>\d+)/$', views.EditTask,name="edit_task"),
    url('edit_friendtask/(?P<id_task>\d+)/$', views.EditTask2,name="edit_task2"),
    url('edit_unfollowtask/(?P<id_task>\d+)/$', views.EditUnfollow,name="edit_unfollow"),

    # # ******************************** bot url's ************************************************************
    url('start-bot/$', views.StartBot.as_view(),name='start'),
    url('start/(?P<task>\d+)/$', views.start,name='starter'),
    url('stop-bot/(?P<t>\d+)/$', views.detener, name='detener'),
    url('imprimir/$', views.pruebaimpresion, name='impresion'),
    url('generate/$', views.GenerateRandomUserView.as_view(), name='generate')


]
