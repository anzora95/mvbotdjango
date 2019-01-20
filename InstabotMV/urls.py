from django.conf.urls import url
from django.urls import path
from . import views
from InstabotMV.views import MediaList



app_name = 'instabot'

urlpatterns = [
    url('show/(?P<username_url>\w+)/$', views.ShowView.as_view(), name='show'),
    url('login/$', views.LoginView.as_view(), name='login'),
    url('logout/$', views.logout, name='logout'),
    url('dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url('dashboard/$', views.tag_child, name='dashload'),
    url('dashboard/task/new$', views.NewTask.as_view(), name='newTask'),
    url('dashboard/task/new/follow-like/$', views.NewFollowLike.as_view(), name='newFollowLike'),
    url('dashboard/task/new/unfollow-task/$', views.UnfollowTask.as_view(), name='unfollow_task'),
    url('dashboard/accounts/$', views.UserAccounts.as_view(), name='userAccounts'),
    url('create/$', views.Create.as_view(), name='create'),
    url('store-new-task/$', views.StoreTask.as_view(), name='storeTask'),
    url('store-new-task-u/$', views.StoreTaskUser.as_view(), name='storeTaskU'),
    # # ******************************** bot url's ************************************************************
    url('start-bot/$', views.StartBot.as_view(), name='start'),
    url('stop-bot/$', views.StopBot.as_view(), name='stopBot'),


]


# url('show/(?P<pk>\d+)/$', views.ShowView.as_view(), name='show'),
# url('dashboard-client/$', views.DashboardClient.as_view(), name='dashboard-client'),


# url('store-new-task-location/$',views.StoreTaskLocation.as_view(),name= 'StoreTaskLocation'),
# url('profile/$', views.Profile.as_view(), name='profile'),
# url('users/$', views.UsersView.as_view(), name='user-list'),
# url('users/manage/(?P<user_id>\d+)/$', views.ManageUsers.as_view(), name='manage'),
# url('users/manage/edit/(?P<pk>\d+)/$', views.UserUpdate.as_view(), name='edit_profile'),
# url('users/manage/delete/(?P<pk>\d+)/$', views.UserDelete.as_view(), name='delete-system-user'),

# url('mybot/$', views.MyBot.as_view(), name='mybot'),

# url('comment-list/$', views.CommentList.as_view(), name='comment-list'),
# url('black-list/$', views.BlackList.as_view(), name='blacklist'),
#url('leer-tags/$', views.hashtag_read(), name='leerhashtags'),