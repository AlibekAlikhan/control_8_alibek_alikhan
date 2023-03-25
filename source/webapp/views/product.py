from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView
from django.db.models import Q
from webapp.forms import ProductForm

from webapp.models import Product

from webapp.forms import SearchForm

from webapp.forms import CommentForm

from webapp.models import Comment


class ProductView(ListView):
    template_name = "product.html"
    model = Product
    context_object_name = "tasks"
    ordering = ['-create_at']
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['favorit_form'] = CommentForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(iis_deleted=True)


class ProductCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    template_name = "product_create.html"
    model = Product
    form_class = ProductForm

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Moderator']).exists()

    def get_success_url(self):
        return reverse_lazy('detail_view', kwargs={'pk': self.object.pk})


class ProductUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "product_update.html"
    form_class = ProductForm
    context_object_name = 'task'


    def test_func(self):
        return self.request.user.groups.filter(name__in=['Moderator']).exists()



    def get_success_url(self):
        return reverse_lazy('detail_view', kwargs={'pk': self.object.pk})


class ProductDetailView(TemplateView):
    template_name = "detail_product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Product, pk=kwargs['pk'])
        comment = Q(product=get_object_or_404(Product, pk=kwargs['pk']))
        context['comment'] = Comment.objects.filter(comment)
        return context


class ProductDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    template_name = 'delete_confirm.html'
    model = Product
    context_object_name = 'task'
    success_url = reverse_lazy('index_article')

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Moderator']).exists()

    def get(self, request, *args, **kwargs):
        return self.delete(request)
