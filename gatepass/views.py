from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from .models import GatePass, UserProfile
from .serializers import UserRegistrationSerializer, UserSerializer, GatePassSerializer, GatePassUpdateSerializer

# Custom permission to check if user is admin
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.userprofile.role == 'admin'

# User Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

# Current User Info
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# Gate Pass CRUD
class GatePassListCreateView(generics.ListCreateAPIView):
    serializer_class = GatePassSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.userprofile.role == 'admin':
            return GatePass.objects.all()
        else:
            return GatePass.objects.filter(user=user)

class GatePassUpdateView(generics.UpdateAPIView):
    queryset = GatePass.objects.all()
    serializer_class = GatePassUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    http_method_names = ['patch']

# Dashboard Statistics
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    today = timezone.now().date()
    this_month_start = today.replace(day=1)
    
    if user.userprofile.role == 'admin':
        # Admin sees all stats
        pending_count = GatePass.objects.filter(status='pending').count()
        approved_today = GatePass.objects.filter(
            status='approved', 
            created_at__date=today
        ).count()
        total_this_month = GatePass.objects.filter(
            created_at__date__gte=this_month_start
        ).count()
    else:
        # Students see only their stats
        pending_count = GatePass.objects.filter(user=user, status='pending').count()
        approved_today = GatePass.objects.filter(
            user=user,
            status='approved', 
            created_at__date=today
        ).count()
        total_this_month = GatePass.objects.filter(
            user=user,
            created_at__date__gte=this_month_start
        ).count()
    
    return Response({
        'pending_requests': pending_count,
        'approved_today': approved_today,
        'total_this_month': total_this_month
    })