from django.contrib import admin

from content.models import Post, Language, Category, SubCategory, PostNode, PostCard, Update, Comment, CommentCard, Dependency, Troubleshooting, Issue


class PostAdmin(admin.ModelAdmin):
    #date_hierarchy = "created_at"
    #field = ("published", "title", "slug", "updated_at", "author")
    #list_display = ["published", "title", "updated_at"]
    #list_display_links = ["title"]
    #list_editable = ["published"]
    #list_filter = ["published", "updated_at", "author"]
    prepopulated_fields = {"slug": ("title",)}
    #search_fields = ["title", "content"]

class PostCardAdmin(admin.ModelAdmin):
    #date_hierarchy = "created_at"
    field = ("title", "slug", "updated_at", "author")
    list_display = ["title", "updated_at"]
    list_display_links = ["title"]
    #list_editable = ["published"]
    #list_filter = ["published", "updated_at", "author"]
    #prepopulated_fields = {"slug": ("title",)}
    #search_fields = ["title", "content"]

class UpdateAdmin(admin.ModelAdmin):
    pass


class IssueAdmin(admin.ModelAdmin):
    pass


class TroubleshootingAdmin(admin.ModelAdmin):
    pass


class DependencyAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


class CommentCardAdmin(admin.ModelAdmin):
    pass


class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    #date_hierarchy = "title"

class PostNodeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["slug"]
    #date_hierarchy = "title"


class LanguageAdmin(admin.ModelAdmin):
    #date_hierarchy = "updated_at"
    #field = ("published", "title", "slug", "updated_at", "author")
    #list_display = ["published", "title", "updated_at"]
    #list_display_links = ["title"]
    #list_editable = ["published"]
    #list_filter = ["published", "updated_at", "author"]
    prepopulated_fields = {"slug": ("name",)}
    #search_fields = ["title", "content"]


admin.site.register(Post, PostAdmin)
admin.site.register(PostCard, PostCardAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(PostNode, PostNodeAdmin)
admin.site.register(Update, UpdateAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentCard, CommentCardAdmin)
admin.site.register(Dependency, DependencyAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Troubleshooting, TroubleshootingAdmin)


