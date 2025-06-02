from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_home(request):
    return JsonResponse({
        'message': 'E-Material Gate Pass API is running!',
        'endpoints': {
            'admin': '/admin/',
            'register': '/api/auth/register/',
            'login': '/api/auth/jwt/create/',
            'gatepasses': '/api/gatepasses/',
            'dashboard': '/api/dashboard/stats/'
        },
        'status': 'Backend Ready for Frontend Connection! 🚀'
    })

urlpatterns = [
    path('', api_home, name='api-home'),
    path('admin/', admin.site.urls),
    path('api/', include('gatepass.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
]