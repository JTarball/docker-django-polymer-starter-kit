from __future__ import unicode_literals

import logging
from inspect import ismethod

from django.core.urlresolvers import (reverse, resolve, NoReverseMatch,
                                      Resolver404)
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from django.db.models import Model
from django import template

from django import template
from django.core.urlresolvers import reverse_lazy

from content.models import Language, Category

# Get instance of logger
logger = logging.getLogger('project_logger')

register = template.Library()


CONTEXT_KEY = 'DJANGO_BREADCRUMB_LINKS'
MAX_WIDTH_BREADCRUMBS=1200
MAX_WIDTH_BREADCRUMB=200

@register.simple_tag(takes_context=True)
def render_breadcrumbs(context, *args):
    """
        Render breadcrumbs html using twitter bootstrap css classes.

        NOTE: Breadcrumb MUST end with a '/'
    """
    if not 'request' in context:
        logger.error("request object not found in context! Check if 'django.core.context_processors.request'\
                      is in TEMPLATE_CONTEXT_PROCESSORS")
        return ''

    logger.info('This is path: %s' % context['request'].path)
    current_app = context['request'].resolver_match.namespace
    print current_app
    #url = reverse(viewname="content:python", current_app=current_app)
    #print url
    # remove trailing /  
    links=[]
    href=""
    for url in context['request'].path.lstrip('/').rstrip('/').split('/'):
        href += url + '/'
        links.append((href, _(smart_text(url)) if url else url))

    orig_links = links

    print links
    # HACK: FOR MAX LENGTH OF BREADCRUMBS for rendering 
    # Here we change the start to ...
    if len(links) >  (MAX_WIDTH_BREADCRUMBS/MAX_WIDTH_BREADCRUMB):
        #logger.info('len links: %s %s', len(links), links)
        #print "max ", (MAX_WIDTH_BREADCRUMBS/MAX_WIDTH_BREADCRUMB)
        no_to_remove = len(links) - (MAX_WIDTH_BREADCRUMBS/MAX_WIDTH_BREADCRUMB)
        #print no_to_remove
        #for i in range(len(links)):
        #    print links[i]
        href = links[no_to_remove-1][0]
        del links[0:no_to_remove]
        links.insert(0, (href, "..."))


    if not links: return ''
    return mark_safe(template.loader.render_to_string(
        'blog/breadcrumbs.html', {'breadcrumbs': links,
                        'breadcrumbs_total': len(orig_links)}))

