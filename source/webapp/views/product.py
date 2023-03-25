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

from webapp.forms import ProjectForm

from webapp.models import Project


class ArticleView(ListView):
    template_name = "product.html"
    model = Task
    context_object_name = "tasks"
    ordering = ['-create_at']
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['favorit_form'] = ProjectForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(iis_deleted=True)


class ArticleCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    template_name = "product_create.html"
    model = Task
    form_class = ArticleForm

    def test_func(self):
        return self.request.user.groups.filter(name__in=['admins']).exists()

    def get_success_url(self):
        return reverse_lazy('detail_view', kwargs={'pk': self.object.pk})


class ArticleUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "product_update.html"
    form_class = ArticleForm
    context_object_name = 'task'


    def test_func(self):
        return self.request.user.groups.filter(name__in=['admins']).exists()



    def get_success_url(self):
        return reverse_lazy('detail_view', kwargs={'pk': self.object.pk})


class ArticleDetailView(TemplateView):
    template_name = "detail_product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=kwargs['pk'])
        comment = Q(product=get_object_or_404(Task, pk=kwargs['pk']))
        context['comment'] = Project.objects.filter(comment)
        return context


class ArticleDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    template_name = 'delete_confirm.html'
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('index_article')

    def test_func(self):
        return self.request.user.groups.filter(name__in=['admins']).exists()

    def get(self, request, *args, **kwargs):
        return self.delete(request)
