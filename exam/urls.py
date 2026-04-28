from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('payment/', views.payment_view, name='payment'),
    path('exam/', views.exam_view, name='exam'),
    path('result/', views.result_view, name='result'),
    path('logout/', views.logout_view, name='logout'),

    # admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve-payment/<int:id>/', views.approve_payment, name='approve_payment'),
    path('check-response/<int:student_id>/', views.check_response, name='check_response'),
    path('publish-result/<int:id>/', views.publish_result, name='publish_result'),
]