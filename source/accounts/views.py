from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DeleteView

from accounts.forms import LoginForm

from accounts.forms import CustomUserCreation

from accounts.forms import UserAdd

from webapp.models import Project


class LoginView(TemplateView):
    template_name = "login.html"
    form = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form()
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            redirect('index_article')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            redirect('index_article')
        login(request, user)
        next = request.GET.get('next')
        if next:
            return redirect(next)
        return redirect('index_article')


def logout_view(request):
    logout(request)
    return redirect('index_article')


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreation
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(self.success_url)
        context = {'form': form}
        return self.render_to_response(context)


class AddUserView(UserPassesTestMixin, CreateView):
    template_name = 'users.html'
    success_url = '/'

    def test_func(self):
        project_user = Project.objects.get(pk=self.kwargs.get('pk'))
        users = project_user.users.all()
        for i in users:
            if self.request.user == i:
                return self.request.user.groups.filter(name__in=['Project Manager', 'Team Lead']).exists()

    def get(self, request, *args, **kwargs):
        form = self.get_user_form()
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.get_user_form()
        if form.is_valid():
            project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
            project.users.add(form.cleaned_data.get('user'))
            return redirect(self.success_url)
        context = {'form': form}
        return self.render_to_response(context)

    def get_user_form(self):
        return UserAdd(self.request.POST)


class UserDeleteView(UserPassesTestMixin, DeleteView):
    model = User
    success_url = '/'

    def test_func(self):
        project_user = Project.objects.get(pk=self.kwargs.get('pk'))
        for i in project_user.users.all():
            if self.request.user == i:
                return self.request.user.groups.filter(name__in=['Project Manager', 'Team Lead']).exists()

    def get(self, request, *args, **kwargs):
        return self.delete(request)


class UserView(ListView):
    template_name = 'users.html'
    context_object_name = 'users'
    model = User

    def get_queryset(self):
        return User.objects.all()
