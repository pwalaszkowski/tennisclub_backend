from django.urls import path
from .views import RegisterUserView, LoginView, HomeView, LogoutView, CustomTokenRefreshView, ClubUserListView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('users/', ClubUserListView.as_view(), name='user-list'),

]
