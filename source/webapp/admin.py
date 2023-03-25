from django.contrib import admin

from webapp.models import Product

from webapp.models import Comment


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "create_at")
    list_filter = ("id", "create_at")
    search_fields = ("text",)
    filter = ("text", "create_at")
    readonly_fields = ("id", "create_at")


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    filter = ["name"]
    readonly_fields = ["id"]


admin.site.register(Product, ArticleAdmin)
admin.site.register(Comment, ProjectAdmin)
