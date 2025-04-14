from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('test/', views.test_template, name='test'),
    path('apply/', views.loan_application, name='apply'),
    path('applications/', views.loan_applications, name='applications'),
    path('application/<int:pk>/', views.loan_application_detail, name='application_detail'),
    path('repayments/', views.repayments, name='repayments'),
] 