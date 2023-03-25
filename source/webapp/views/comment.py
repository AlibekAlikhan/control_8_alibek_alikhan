from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DeleteView, FormView

from webapp.forms import CommentForm
from webapp.models import Comment

from webapp.models import Product


class CommentView(UserPassesTestMixin, LoginRequiredMixin, FormView):
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            text_comment = form.cleaned_data.get('text_comment')
            grade = form.cleaned_data.get('grade')
            user = request.user
            Comment.objects.create(users=user, product=product, text_comment=text_comment, grade=grade)
        return redirect('index_article')

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Moderator', 'users']).exists()


class CommentUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'update_comment.html'
    form_class = CommentForm
    context_key = 'project'


    def test_func(self):
        return self.request.user.groups.filter(name__in=['Moderator', 'users']).exists()

    def get_success_url(self):
        return reverse_lazy('index_article')


class CommentDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    template_name = 'delit_comment.html'
    model = Comment
    context_object_name = 'project'
    success_url = reverse_lazy('index_article')

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Moderator', 'users']).exists()

    def get(self, request, *args, **kwargs):
        return self.delete(request)
