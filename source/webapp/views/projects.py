from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, DeleteView

from webapp.forms import ProjectForm
from webapp.models import Project


class ProjectCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    template_name = "project_create.html"
    model = Project
    form_class = ProjectForm

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Project Manager']).exists()

    def get_success_url(self):
        return reverse_lazy("project_index")


class ProjectDetailView(DetailView):
    template_name = 'project_detail.html'
    model = Project


class ProjectView(ListView):
    template_name = 'project.html'
    context_object_name = 'project'
    model = Project

    def get_queryset(self):
        return Project.objects.exclude(iis_deleted=True)


class ProjectUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'update_project.html'
    form_class = ProjectForm
    context_key = 'project'

    def test_func(self):
        return self.request.user.groups.filter(
            name__in=['Project Manager']).exists() and self.request.user in Project.objects.get(
            pk=self.kwargs['pk']).users.all()

    def get_success_url(self):
        return reverse_lazy('detail_project', kwargs={'pk': self.object.pk})


class ProjectDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    template_name = 'delit_project.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('project_index')

    def test_func(self):
        return self.request.user.groups.filter(
            name__in=['Project Manager']).exists() and self.request.user in Project.objects.get(
            pk=self.kwargs['pk']).users.all()

    def get(self, request, *args, **kwargs):
        return self.delete(request)
