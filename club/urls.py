from django.urls import path
from .views import RegisterUserView, LoginView, HomeView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
