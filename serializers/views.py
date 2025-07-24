from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens(user)
            return Response({'user': UserSerializer(user).data, 'tokens': tokens})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens(user)
            return Response({'user': UserSerializer(user).data, 'tokens': tokens})
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class CheckEmailView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        exists = User.objects.filter(email=email).exists()
        return Response({'exists': exists})

class GoogleSignInView(APIView):
    def post(self, request):
        email = request.data.get('email')
        name = request.data.get('name')
        if not email or not name:
            return Response({"error": "Missing fields"}, status=400)

        try:
            user = User.objects.get(email=email)
            user.name = name
            user.is_google = True
            user.save()
        except User.DoesNotExist:
            return Response({"error": "Please create an account first"}, status=404)

        tokens = get_tokens(user)
        return Response({'user': UserSerializer(user).data, 'tokens': tokens})
