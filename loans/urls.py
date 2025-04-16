from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('test/', views.test_template, name='test'),
    path('apply/', views.loan_application, name='apply'),
    path('apply/<int:property_id>/', views.loan_application, name='apply_with_property'),
    path('applications/', views.loan_applications, name='applications'),
    path('application/<int:pk>/', views.loan_application_detail, name='application_detail'),
    path('application/<int:pk>/edit/', views.loan_application_edit, name='application_edit'),
    path('application/<int:pk>/cancel/', views.loan_application_cancel, name='application_cancel'),
    path('repayments/', views.loan_repayments, name='repayments'),
    path('repayment/<int:pk>/', views.loan_repayment_detail, name='repayment_detail'),
    path('repayment/<int:pk>/pay/', views.loan_repayment_pay, name='repayment_pay'),
] 