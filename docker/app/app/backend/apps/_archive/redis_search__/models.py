from django.db import models

#@Redis_Search("name") # need to add the keyword + prefixes and then search for all urls
#class RedisKeyword(models.Model):
#    """ model has been simplified for brevity """
#    name = models.CharField(('title'), max_length=200)
#    #manual_added_urls = 
#    class Meta:
#        db_table = 'keywords'   # name in the database
#        verbose_name_plural = 'keywords' 
#    
#    def __unicode__(self):
#        return self.name # return a string representation of our model    


#class KeywordGroup(models.Model):
#    name = models.CharField(('title'), max_length=200)
#    keywords = models.ManyToManyField(RedisKeyword)
    
#    class Meta:
#        db_table = 'keyword_groups'   # name in the database
#        verbose_name_plural = 'keyword_groups' 
#    
#    def __unicode__(self):
#        return self.name # return a string representation of our model