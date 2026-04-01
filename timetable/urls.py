from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable_list, name='timetable_list'),
    path('add-timetable/', views.add_timetable, name='add_timetable'),
    path('visual-tool/', views.visual_timetabling_embed, name='visual_tool'),
    path('export-json/', views.export_timetable_json, name='export_json'),

    # PROPOSALS
    path('add-proposal/', views.add_proposal, name='add_proposal'),
    path('proposals/', views.proposal_list, name='proposal_list'),
    path('proposal/<int:proposal_id>/approve/', views.approve_proposal, name='approve_proposal'),
    path('proposal/<int:proposal_id>/reject/', views.reject_proposal, name='reject_proposal'),
    path('get-department-data/<int:dept_id>/', views.get_department_data, name='get_department_data'),
]