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


@register.simple_tag(takes_context=True)
def show_menu(context):
    categories = [cat.slug for cat in Category.objects.all()]
    path= context['request'].path
    return {'categories': categories,'path':path}

@register.inclusion_tag('navbar.html', takes_context=True)
def show_categories(context):
    categories = [cat for cat in Category.objects.all()]
    path= context['request'].path
    print "show_categoried --- path", path
    return {'categories': categories, 'path':path}

@register.inclusion_tag('navbar.html', takes_context=True)
def show_navbar(context):
    languages = [lang for lang in Language.objects.all()]
    categories = [cat for cat in Category.objects.all()]
    subcategories = []# [subcat for subcat in SubCategory.objects.all()]
    path = context['request'].path
    return { 'languages': languages, 'categories': categories, 'subcategories':subcategories, 'path':path, 'path_lang':context['path_language'], 'path_cat':context['path_category'], 'path_subcat':context['path_subcategory'] }


@register.simple_tag(takes_context=True)
def active_page(context, req):
    request = context['request']
    #print "path", request
    #if not request:
    #   	logger.error('Cant find request - needed for active page css') 
    logger.error('dsfds %s' % request.path)
    return "active"
    #try:
    #    return "active"
        #return "active" if resolve(request.path_info).url_name == view_name else ""
    #except Resolver404:
    #    return ""


@register.filter(name='is_empty')
def is_empty(value):
    """ Checks whether value is empty. Should be string. """
    logger.info('is_empty value:%s' % value )
    if not value.strip(' '):
        return True
    else:
        return False



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
        logger.error("request object not found in context! Check if "
                     "'django.core.context_processors.request' is in "
                     "TEMPLATE_CONTEXT_PROCESSORS")
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
        'navbar.html', {'breadcrumbs': links,
                        'breadcrumbs_total': len(orig_links)}))




    # if args:
    #     template_path = args[0]
    # else:
    #     template_path = 'django_bootstrap_breadcrumbs/bootstrap2.html'
    # print "befor elubjkks [p"
    # links = []
    # for (label, viewname, view_args) in context['request'].META.get(CONTEXT_KEY, []):
    #     if isinstance(viewname, Model) and hasattr(
    #             viewname, 'get_absolute_url') and ismethod(
    #             viewname.get_absolute_url):
    #         url = viewname.get_absolute_url()
    #         print "fndsnflksnkfnsdjdjdjjdpopopopop"
    #     else:
    #         try:
    #             try:
    #                 # 'resolver_match' introduced in Django 1.5
    #                 current_app = context['request'].resolver_match.namespace
    #                 logger.info('%s' % current_app)
    #             except AttributeError:
    #                 try:
    #                     resolver_match = resolve(context['request'].path)
    #                     print resolver_match, "jkjdlsfjjlsdkjlfkjlskjfljsdljfldjslkjfkldsj"
    #                     current_app = resolver_match.namespace
    #                     logger.info('%s' % current_app)
    #                 except Resolver404:
    #                     print '404'
    #                     current_app = None
    #             url = reverse(viewname=viewname, args=view_args,
    #                           current_app=current_app)
    #         except NoReverseMatch:
    #             url = viewname
    #     links.append((url, _(smart_text(label)) if label else label))
    # logger.warning('fdskljfldsjlkfjdkls %s' % links )
    # if not links:
    #     return ''

    # return mark_safe(template.loader.render_to_string(
    #     template_path, {'breadcrumbs': links,
    #                     'breadcrumbs_total': len(links)}))



