from django import template
from django.contrib.flatpages.models import FlatPage

register = template.Library()


@register.inclusion_tag("redis_search/index.html")
def search_links():
    return None
    #flatpage_list = FlatPage.objects.all()
    #return {'flatpage_list': flatpage_list}