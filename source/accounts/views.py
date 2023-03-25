from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, UpdateView

from accounts.forms import LoginForm

from accounts.forms import CustomUserCreation

from accounts.forms import UserAdd

from webapp.models import Project

from accounts.forms import ProfileChangeForm, UserChangeForm


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
        return self.request.user.groups.filter(name__in=['Project Manager', 'Team Lead']).exists()

    def get(self, request, *args, **kwargs):
        return self.delete(request)


class UserView(ListView):
    template_name = 'users.html'
    context_object_name = 'users'
    model = User

    def get_queryset(self):
        return User.objects.all()


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    paginate_related_by = 3
    paginate_related_orphans = 0

    # def get_context_data(self, **kwargs):
    #     articles = self.model
    #     paginator = Paginator(articles, self.paginate_related_by,
    #                           orphans=self.paginate_related_orphans)
    #     page_number = self.request.GET.get('page', 1)
    #     page = paginator.get_page(page_number)
    #     kwargs['page_obj'] = page
    #     kwargs['articles'] = page.object_list
    #     kwargs['is_paginated'] = page.has_other_pages()
    #     return super().get_context_data(**kwargs)


class UserChangeView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()

        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        return self.form_invalid(form, profile_form)

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response
