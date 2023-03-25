from django.urls import path

from webapp.views.tasks import ArticleView, ArticleCreateView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView

from webapp.views.projects import ProjectCreateView, ProjectDetailView, ProjectView, ProjectUpdateView, ProjectDeleteView


urlpatterns =[
    path('', ArticleView.as_view(), name="index_article"),
    path('article', ArticleView.as_view(), name="index_article"),
    path('article/create', ArticleCreateView.as_view(), name="create_article"),
    path('article/<int:pk>', ArticleDetailView.as_view(), name="detail_view"),
    path('article/<int:pk>/update', ArticleUpdateView.as_view(), name="article_update"),
    path('article/<int:p_pk>/delit', ArticleDeleteView.as_view(), name="article_delit"),
    path('article/<int:pk>/delit/confirm', ArticleDeleteView.as_view(), name="confirm"),
    path('project/create', ProjectCreateView.as_view(), name="create_project"),
    path('project/<int:pk>', ProjectDetailView.as_view(), name="detail_project"),
    path('project', ProjectView.as_view(), name="project_index"),
    path('update_project/<int:pk>', ProjectUpdateView.as_view(), name="project_update"),
    path('article/<int:pk>/delit/confirm', ProjectDeleteView.as_view(), name="confirm_project"),
    path('project/<int:pk>/delit', ProjectDeleteView.as_view(), name="project_delit"),
]