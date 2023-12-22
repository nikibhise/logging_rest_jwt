from django.urls import path
from .views import EmployeeAPI, EmployeeDetailsAPI

urlpatterns = [
    path('employees/', EmployeeAPI.as_view()),
    path('employees/<int:pk>/', EmployeeDetailsAPI.as_view()),
    
]