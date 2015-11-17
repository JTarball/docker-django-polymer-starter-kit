from django.contrib import admin

from blog.models import Post, Update, Category


class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    #field = ("published", "title", "slug", "updated_at", "author")
    #list_display = ["published", "title", "updated_at"]
    #list_display_links = ["title"]
    #list_editable = ["published"]
    #list_filter = ["published", "updated_at", "author"]
    prepopulated_fields = {"slug": ("title",)}
    #search_fields = ["title", "content"]


class CategoryAdmin(admin.ModelAdmin):
    pass
    #date_hierarchy = "title"


class UpdateAdmin(admin.ModelAdmin):
    date_hierarchy = "updated_at"
    #field = ("published", "title", "slug", "updated_at", "author")
    #list_display = ["published", "title", "updated_at"]
    #list_display_links = ["title"]
    #list_editable = ["published"]
    #list_filter = ["published", "updated_at", "author"]
    #prepopulated_fields = {"slug": ("title",)}
    #search_fields = ["title", "content"]


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Update, UpdateAdmin)
