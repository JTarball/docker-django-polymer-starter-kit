import logging
import re

from sets import Set

from django.contrib import admin

from taggit.models import Tag

from blog.models import Post, PostRevision, PostNode, Comment, VirtualTag

# Get instance of logger
logger = logging.getLogger('project_logger')

def excluding_tags(instance):
    print excluding_tags
    return ', '.join(instance.excluding_tags)
    

class PostAdmin(admin.ModelAdmin):
    #date_hierarchy = "created_at"
    field = ("published", "slug")
    #list_display = ["published", "title", "updated_at"]
    #list_display_links = ["title"]
    #list_editable = ["published"]
    #list_filter = ["published", "updated_at", "author"]
    prepopulated_fields = {"slug": ("title",)}
    #list_display = ['title', excluding_tags]
    #search_fields = ["title", "content"]

    def save_related(self, request, form, formsets, change):
        super(PostAdmin, self).save_related(request, form, formsets, change)
        # TODO: If you change this you need to change models.py 
        #       This is not ideal.
        if form.instance.pk:
            # Include any manual tags
            default_tags = []
            if form.instance.include_tags:
                default_tags = [tag.name for tag in form.instance.include_tags.all()]
            default_tags.extend([form.instance.node.name.lower(), form.instance.node.parent.name.lower()])
            contTags = Set(default_tags)

            # Find any tags from content and auto-add
            for tag in Tag.objects.all():
                if re.search( tag.name, form.instance.content, re.M|re.I):
                    contTags.add(tag)

            # Finally remove any tags which are from exclude tags
            if form.instance.exclude_tags:
                exclude_tags = [exclude_tag.name for exclude_tag in form.instance.exclude_tags.all()]
                contTags = Set([tag for tag in contTags if tag not in exclude_tags])

            form.instance.tags.clear()
            for tag in contTags:
                form.instance.tags.add(tag)

            logger.info('save_related %s' % form.instance.comments.all() )
            PostRevision.objects.create_post_revision(post=form.instance, content=form.instance.content, comment=form.instance.update_comment)


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



#class TaggedItemInline(admin.StackedInline):
#    model = TaggedItem

class VirtualTagAdmin(admin.ModelAdmin):
#    inlines = [
#        TaggedItemInline
#    ]
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(VirtualTag, VirtualTagAdmin)




admin.site.register(Post, PostAdmin)
#admin.site.register(PostCard, PostCardAdmin)
#admin.site.register(Category, CategoryAdmin)
#admin.site.register(SubCategory, SubCategoryAdmin)
#admin.site.register(Language, LanguageAdmin)
admin.site.register(PostNode, PostNodeAdmin)
#admin.site.register(Update, UpdateAdmin)
admin.site.register(Comment, CommentAdmin)
#admin.site.register(CommentCard, CommentCardAdmin)
#admin.site.register(Dependency, DependencyAdmin)
#admin.site.register(Issue, IssueAdmin)
#admin.site.register(Troubleshooting, TroubleshootingAdmin)


