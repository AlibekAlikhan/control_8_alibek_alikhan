from django.urls import path

from accounts.views import LoginView

from accounts.views import logout_view

from accounts.views import RegisterView

from accounts.views import AddUserView, UserDeleteView

urlpatterns =[
    path('login/', LoginView.as_view(), name="login"),
    path('login/logout', logout_view, name="logout"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/<int:pk>/users', AddUserView.as_view(), name="users_view"),
    path('article/<int:pk>/delit', UserDeleteView.as_view(), name="user_delit")
    ]