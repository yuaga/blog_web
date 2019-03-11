from django.urls import path
from . import views

app_name = 'news'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('news_list/', views.news_list_view, name='news_list'),
    path('news_detail/<int:news_id>', views.news_detail_view, name='news_detail'),
    path('news_comment/', views.news_comment_view, name='news_comment'),
    path('personal_space/', views.personal_space_view, name='personal_space'),
    path('web_discuss/', views.comment_view, name='web_discuss'),
]
