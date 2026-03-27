# faculty/urls.py


from django.urls import path
from . import views
urlpatterns = [
 path('', views.index, name='index'),
 path('dashboard/', views.dashboard, name='dashboard'),
 path('tests/ui/', views.ui_test, name='ui_tests'),
]
