from django.urls import path

from accounts.views import LoginView

from accounts.views import logout_view

urlpatterns =[
    path('login/', LoginView.as_view(), name="login"),
    path('login/logout', logout_view, name="logout"),
    ]