from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import User
from .serializers import UserSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email)
        if check_password(password, user.password):
            return Response({
                "token": "dummy-token",  # For now, hardcoded (JWT can be added later)
                "user": UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def check_email(request):
    email = request.query_params.get('email')
    exists = User.objects.filter(email=email).exists()
    return Response({'exists': exists})

@api_view(['POST'])
def google_signin(request):
    email = request.data.get('email')
    name = request.data.get('name')
    if not email or not name:
        return Response({'error': 'Missing email or name'}, status=status.HTTP_400_BAD_REQUEST)

    user, _ = User.objects.get_or_create(
        email=email,
        defaults={'name': name, 'password': '', 'is_google': True}
    )
    return Response({
        "token": "google-token",  # Optional: Google ID token or dummy
        "user": UserSerializer(user).data
    })

@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    # In real app: send reset link
    if User.objects.filter(email=email).exists():
        return Response({'message': 'Password reset link sent to email'})
    return Response({'message': 'If your email exists, a reset link will be sent'})
