from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/user/', views.current_user, name='current-user'),
    
    # Gate Pass Management
    path('gatepasses/', views.GatePassListCreateView.as_view(), name='gatepass-list-create'),
    path('gatepass/<int:pk>/', views.GatePassUpdateView.as_view(), name='gatepass-update'),
    
    # Dashboard
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
]