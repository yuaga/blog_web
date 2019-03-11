from django.urls import path
from apps.cms import views

app_name = 'cms'

urlpatterns = [
    path('index/', views.cms_index, name='index'),
    path('news_category/', views.cms_news_category, name='news_category'),
    path('write_news/', views.CmsWriteNews.as_view(), name='write_news'),
    path('news_manage/', views.CmsNewsManage.as_view(), name='news_manage'),
    path('del_news/', views.cms_del_news_view, name='del_news'),
    path('edit_news/', views.CmsNewsEdit.as_view(), name='edit_news'),
    path('staff_manage/', views.cms_staff_manage, name='staff_manage'),
    path('add_category/', views.cms_add_category, name='add_category'),
    path('edit_category/', views.cms_edit_category, name='edit_category'),
    path('del_category/', views.cms_del_category, name='del_category'),
    path('upload_file/', views.upload_file_view, name='upload_file'),
]
