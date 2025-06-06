# gatepass/views.py - Fixed version to handle authentication properly

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import GatePass, UserProfile
from .serializers import (
    UserRegistrationSerializer, 
    UserSerializer, 
    GatePassSerializer, 
    GatePassUpdateSerializer
)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class GatePassListCreateView(generics.ListCreateAPIView):
    serializer_class = GatePassSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # FIXED: Check if user is authenticated first
        if not user.is_authenticated:
            return GatePass.objects.none()
        
        try:
            # FIXED: Handle case where UserProfile might not exist
            user_profile = getattr(user, 'userprofile', None)
            if user_profile and user_profile.role == 'admin':
                return GatePass.objects.all()
            else:
                return GatePass.objects.filter(user=user)
        except Exception as e:
            # Log the error and return empty queryset
            print(f"Error accessing user profile: {e}")
            return GatePass.objects.none()
    
    def create(self, request, *args, **kwargs):
        # FIXED: Add better error handling for creation
        try:
            # Ensure user is authenticated
            if not request.user.is_authenticated:
                return Response(
                    {'error': 'Authentication required'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Create the gate pass
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response(
                {'error': f'Server error: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GatePassDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GatePassSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if not user.is_authenticated:
            return GatePass.objects.none()
            
        try:
            user_profile = getattr(user, 'userprofile', None)
            if user_profile and user_profile.role == 'admin':
                return GatePass.objects.all()
            else:
                return GatePass.objects.filter(user=user)
        except Exception:
            return GatePass.objects.none()

class GatePassUpdateStatusView(generics.UpdateAPIView):
    serializer_class = GatePassUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Only admins can update status
        user = self.request.user
        
        if not user.is_authenticated:
            return GatePass.objects.none()
            
        try:
            user_profile = getattr(user, 'userprofile', None)
            if user_profile and user_profile.role == 'admin':
                return GatePass.objects.all()
            else:
                return GatePass.objects.none()
        except Exception:
            return GatePass.objects.none()

# BONUS: Add a debug view to test authentication
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def debug_user_info(request):
    """Debug endpoint to check user authentication and profile"""
    user = request.user
    
    try:
        user_profile = getattr(user, 'userprofile', None)
        
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'is_authenticated': user.is_authenticated,
            'has_profile': user_profile is not None,
            'role': user_profile.role if user_profile else 'No profile',
            'message': 'Authentication working correctly!'
        })
    except Exception as e:
        return Response({
            'error': str(e),
            'user_id': user.id,
            'username': user.username,
            'is_authenticated': user.is_authenticated,
        })

# BONUS: Health check endpoint
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_check(request):
    """Simple health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'Gate Pass API is running',
        'endpoints': {
            'register': '/api/auth/register/',
            'login': '/api/auth/jwt/create/',
            'gatepasses': '/api/gatepasses/',
            'debug': '/api/debug-user/',
            'health': '/api/health/'
        }
    })