
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('auth/register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('user/profile/', views.UserProfileView.as_view(), name='user-profile'),
    
    # Gate Pass CRUD
    path('gatepasses/', views.GatePassListCreateView.as_view(), name='gatepass-list-create'),
    path('gatepasses/<int:pk>/', views.GatePassDetailView.as_view(), name='gatepass-detail'),
    path('gatepasses/<int:pk>/update-status/', views.GatePassUpdateStatusView.as_view(), name='gatepass-update-status'),
    
    # Debug & Health Check (BONUS)
    path('debug-user/', views.debug_user_info, name='debug-user'),
    path('health/', views.health_check, name='health-check'),
]