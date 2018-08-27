from django.conf.urls import url
from task import views as tv
app_name = 'task'
urlpatterns = [
    url(r'^login/$', tv.login, name='login'),
    url(r'^logout/$', tv.logout, name='logout'),
    url(r'^edition_manage/$', tv.edition_manage, name='edition_manage'),
    url(r'^add_edit_button/(?P<edition_id>[0-9]+)/(?P<flag>[0-9]+)/$', tv.add_edit_button, name='add_edit_button'),
    url(r'^delete_project/(?P<edition_id>[0-9]+)/$', tv.delete_project, name='delete_project'),
    url(r'^search_edition/$', tv.search_edition, name='search_edition'),
    url(r'^task_manage/$', tv.task_manage, name='task_manage'),
    url(r'^add_task/(?P<edition_id>[0-9]+)/(?P<task_id>[0-9]+)/(?P<flag>[0-9]+)/$', tv.add_task, name='add_task'),
    url(r'^search_task/$', tv.search_task, name='search_task'),
]