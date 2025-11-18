# users/auth_views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import User
from .auth_serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'},
                    'new_password': {'type': 'string'},
                },
                'required': ['username', 'password']
            }
        },
        examples=[
            OpenApiExample(
                'Normal Login',
                summary='Standard authentication',
                value={
                    'username': 'string',
                    'password': 'string'
                }
            ),
            OpenApiExample(
                'Password Change',
                summary='Change default password',
                value={
                    'username': 'string',
                    'password': 'string',
                    'new_password': 'string'
                }
            )
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'refresh': {'type': 'string'},
                    'access': {'type': 'string'},
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'first_name': {'type': 'string'},
                            'last_name': {'type': 'string'},
                            'role': {'type': 'string'},
                            'has_default_password': {'type': 'boolean'}
                        }
                    }
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'detail': {'type': 'string'}
                }
            }
        }
    )
    def post(self, request, *args, **kwargs):
        # Check if this is a password change request (has new_password)
        new_password = request.data.get('new_password')
        
        if new_password:
            return self.handle_password_change(request)
        
        # Otherwise, proceed with normal token obtain
        return super().post(request, *args, **kwargs)
    
    def handle_password_change(self, request):
        username = request.data.get('username')
        old_password = request.data.get('password')  # This is the default password
        new_password = request.data.get('new_password')
        
        if not username or not old_password or not new_password:
            return Response(
                {"detail": "username, password (old), and new_password are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify the old/default password
        if not check_password(old_password, user.password):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Change to new password and update flag
        user.set_password(new_password)
        user.has_default_password = False
        user.save()
        
        # Generate new tokens with updated user info
        serializer = self.get_serializer(data={
            'username': username,
            'password': new_password  # Use the new password for token generation
        })
        serializer.is_valid(raise_exception=True)
        
        # Get the updated response with user data
        data = serializer.validated_data
        data['user'] = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "has_default_password": user.has_default_password
        }
        
        return Response(data, status=status.HTTP_200_OK)