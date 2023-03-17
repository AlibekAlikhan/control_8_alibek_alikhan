from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, DeleteView

from webapp.forms import ProjectForm
from webapp.models import Project

from webapp.models import Task


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = "project_create.html"
    model = Project
    form_class = ProjectForm

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


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'update_project.html'
    form_class = ProjectForm
    context_key = 'project'

    def get_success_url(self):
        return reverse_lazy('detail_project', kwargs={'pk': self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'delit_project.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('project_index')

    def get(self, request, *args, **kwargs):
        return self.delete(request)
