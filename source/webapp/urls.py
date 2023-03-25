from django.urls import path

from webapp.views.product import ProductView, ProductCreateView, ProductDetailView, ProductUpdateView, ProductDeleteView

from webapp.views.comment import CommentView, CommentUpdateView, CommentDeleteView


urlpatterns =[
    path('', ProductView.as_view(), name="index_article"),
    path('product', ProductView.as_view(), name="index_article"),
    path('product/create', ProductCreateView.as_view(), name="create_article"),
    path('product/<int:pk>', ProductDetailView.as_view(), name="detail_view"),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name="article_update"),
    path('product/<int:pk>/delit', ProductDeleteView.as_view(), name="article_delit"),
    path('product/<int:pk>/delit/confirm', ProductDeleteView.as_view(), name="confirm"),
    path('comment/<int:pk>', CommentView.as_view(), name="to_comment"),
    path('update_comment/<int:pk>', CommentUpdateView.as_view(), name="project_update"),
    path('comment/<int:pk>/delit/confirm', CommentDeleteView.as_view(), name="confirm_project"),
    path('comment/<int:pk>/delit', CommentDeleteView.as_view(), name="project_delit"),
]