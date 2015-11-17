#Structure of admin



from django.contrib import admin

from redis_search import models as redis_search_models


#class LEDAdmin(admin.ModelAdmin):
#    prepopulated_fields = {"slug": ("name",)} # manually add slug   
#TODO: AUTOMATIC SLUG?

#admin.site.register(redis_search_models.KeywordGroup)
#admin.site.register(redis_search_models.RedisKeyword)

