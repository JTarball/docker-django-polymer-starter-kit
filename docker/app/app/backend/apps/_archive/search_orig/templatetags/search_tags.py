from django import template
from django.contrib.flatpages.models import FlatPage

register = template.Library()

def show_results():
    #choices = poll.choice_set.all()
    return {'choices': 'zxcxzczx'}

# Here, register is a django.template.Library instance, as before
register.inclusion_tag('search/search.html')(show_results)
