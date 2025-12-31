from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Students
    path('students/', views.student_list, name='student_list'),
    path('student/<int:id>/', views.student_detail, name='student_detail'),
    path('add-student/', views.add_student, name='add_student'),  
    path('edit-student/<int:id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),
    
    # Results
    path('results/', views.results_list, name='results_list'),
    path('add-result/', views.add_result, name='add_result'),
    path('edit-result/<int:id>/', views.edit_result, name='edit_result'),
    path('delete-result/<int:id>/', views.delete_result, name='delete_result'),
]
