from django.urls import path

from accounts.views import LoginView

from accounts.views import logout_view

from accounts.views import RegisterView

from accounts.views import AddUserView, UserDeleteView, ProfileView, UserChangeView

urlpatterns =[
    path('login/', LoginView.as_view(), name="login"),
    path('login/logout', logout_view, name="logout"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/<int:pk>/users', AddUserView.as_view(), name="users_view"),
    path('article/<int:pk>/delit', UserDeleteView.as_view(), name="user_delit"),
    path('article/<int:pk>/delit/confirm', UserDeleteView.as_view(), name="user_delit"),
    path('profile/<int:pk>', ProfileView.as_view(), name="profile"),
    path('profile/<int:pk>/change', UserChangeView.as_view(), name="change"),
    ]
