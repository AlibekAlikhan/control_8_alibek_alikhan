from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, DeleteView, FormView

from webapp.forms import ProjectForm
from webapp.models import Project

from webapp.models import Task


class ProjectView(LoginRequiredMixin, FormView):
    form_class = ProjectForm

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Task, pk=kwargs.get('pk'))
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            text_comment = form.cleaned_data.get('text_comment')
            grade = form.cleaned_data.get('grade')
            user = request.user
            Project.objects.create(users=user, product=product, text_comment=text_comment, grade=grade)
        return redirect('index_article')


class ProjectUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'update_comment.html'
    form_class = ProjectForm
    context_key = 'project'


    def test_func(self):
        return self.request.user.groups.filter(name__in=['admins']).exists()

    def get_success_url(self):
        return reverse_lazy('index_article')


class ProjectDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    template_name = 'delit_comment.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('index_article')

    def test_func(self):
        return self.request.user.groups.filter(name__in=['admins']).exists()

    def get(self, request, *args, **kwargs):
        return self.delete(request)
