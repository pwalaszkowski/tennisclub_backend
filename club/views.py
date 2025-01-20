from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework import status, viewsets
from django.shortcuts import redirect

from .models import ClubUser, Court, Reservation
from .serializers import ClubUserSerializer, CourtSerializer, ReservationSerializer


class RegisterUserView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access this view

    def post(self, request):
        serializer = ClubUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access this view

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            # Generate tokens for the authenticated user
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class HomeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Require authentication for this view

    def get(self, request):
        return Response({'message': f'Welcome, {request.user.username}!'})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract the token from the request
            token = request.auth  # DRF automatically sets this if authentication is configured
            if not token:
                return Response({'error': 'No token provided.'}, status=400)

            # Blacklist the token
            token.blacklist()
            return Response({'message': 'Successfully logged out.'}, status=200)
        except AttributeError:
            return Response({'error': 'Invalid token or already logged out.'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class CustomTokenRefreshView(TokenRefreshView):
    """
    A custom refresh view to add any additional logic or data.
    """
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        # You can add custom logic here, like logging or additional response data
        response = super().post(request, *args, **kwargs)
        return response


class ClubUserListView(APIView):
    """
    API view to retrieve all users.
    """
    permission_classes = [IsAuthenticated]  # Require authentication

    def get(self, request):
        users = ClubUser.objects.all()  # Retrieve all users
        serializer = ClubUserSerializer(users, many=True)
        return Response(serializer.data)


class CourtViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Require authentication

    queryset = Court.objects.all()
    serializer_class = CourtSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Require authentication

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        # Limit reservations to the current user
        user = self.request.user
        return Reservation.objects.filter(user=user)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'You have access!'})
