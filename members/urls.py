
from django.urls import path
from . import views
from .views import get_tclass_info

urlpatterns = [
    path('register_member/', views.register_member, name='register_member'),
    path('update_member/', views.update_member, name='update_member'),
    path('update_member_admin/<int:id>/', views.update_member_admin, name='update_member_admin'),
    path('delete_member/<int:id>/', views.delete_member, name='delete_member'),
    path('list_members/', views.list_members, name='list_members'),
    
    path('list_instructors/', views.list_instructors, name='list_instructors'),
    path('create_instructor/', views.create_instructor , name='create_instructor'),
    path('update_instructor/<int:id>/', views.update_instructor, name='update_instructor'),

    path('calendar_instructor/', views.calendar_view, name='calendar_inst'),
    path('instructor_schedule/', views.instructor_schedule_view, name='instructor_schedule'),

    path('list_classes/', views.list_classes, name='list_classes'),
    path('create_class/', views.create_class , name='create_class'),
    path('update_class/<int:id>/', views.update_class, name='update_class'),

    path('list_groups/', views.list_group, name='list_groups'),
    path('create_group/', views.create_group , name='create_group'),
    path('update_group/<int:id>/', views.update_group, name='update_group'),
    path('get_tclass_info/', get_tclass_info, name='get_tclass_info'),
]

