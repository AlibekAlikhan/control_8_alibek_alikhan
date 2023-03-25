from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView
from django.db.models import Q
from webapp.forms import ArticleForm

from webapp.models import Task

from webapp.forms import SearchForm

from webapp.models import Project


class ArticleView(ListView):
    template_name = "tasks.html"
    model = Task
    context_object_name = "tasks"
    ordering = ['-create_at']
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(text__icontains=self.search_value) | Q(detail_text__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.exclude(iis_deleted=True)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class ArticleCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    template_name = "task_create.html"
    model = Task
    form_class = ArticleForm

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Project Manager', 'Team Lead', 'Developer']).exists()

    def get_success_url(self):
        return reverse_lazy('detail_view', kwargs={'pk': self.object.pk})


class ArticleUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "task_update.html"
    form_class = ArticleForm
    context_object_name = 'task'
    # Project.objects.get(
    #     id=self.kwargs['pk'].
    # )
    def test_func(self):
        tasks = Task.objects.get(pk=self.kwargs['pk'])
        return self.request.user.groups.filter(name__in=['Project Manager']).exists() and self.request.user in tasks.project.users.all()

    def get_success_url(self):
        return reverse_lazy('detail_view', kwargs={'pk': self.object.pk})


class ArticleDetailView(TemplateView):
    template_name = "detail_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=kwargs['pk'])
        return context


class ArticleDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    template_name = 'delete_confirm.html'
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('index_article')

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Project Manager', 'Team Lead']).exists()

    def get(self, request, *args, **kwargs):
        return self.delete(request)
