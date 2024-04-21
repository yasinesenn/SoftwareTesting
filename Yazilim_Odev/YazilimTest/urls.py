from django.urls import path
#now import the views.py file into this code
from . import views
urlpatterns=[
  path('repolist/', views.github_repo_list, name='github_repo_list'),
  path('repo/<int:github_repo_id>/', views.java_class_list, name='java_class_list'),
  path('',views.github_depo_ekle,name="anasayfa"),
]