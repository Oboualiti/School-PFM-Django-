from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable_list, name='timetable_list'),
    path('add/', views.add_timetable, name='add_timetable'),
    path('visual-tool/', views.visual_timetabling_embed, name='visual_tool'),
    path('export-json/', views.export_timetable_json, name='export_json'),
]