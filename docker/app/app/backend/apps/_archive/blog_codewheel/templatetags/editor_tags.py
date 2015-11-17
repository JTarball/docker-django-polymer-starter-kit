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

from pygments.styles import STYLE_MAP



#from django import template
#register = template.Library()

# Pygments: http://pygments.org -- a generic syntax highlighter.
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound

# Python Markdown (dropped in my project directory)
from markdown2 import markdown

# BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/
#from BeautifulSoup import BeautifulSoup, Tag
from bs4 import BeautifulSoup

from blog.utils import cwmarkdown

@register.filter
def editor_render(content, safe=False):
    """Render this content for display."""
    return cwmarkdown(content)







def editor_render_unicode(content):
    bs = editor_render(content)
    return unicode(bs)

# create ace editor class for special interactive style
# ace-python, ace-c etc. ?
# create jointjs capability
# only look at content-* ids???
# 





    # markeddown = markdown(unicode(soup), safe_mode=safe)
    # logger.info('Markdown: %s' % markeddown)

    # formatter = HtmlFormatter()


    # soup = BeautifulSoup(unicode(markeddown))
    # code_tags = soup.findAll('code')



    # return soup.prettify()





@register.filter
def editor_rendera(content, safe="unsafe"):
    """Render this content for display."""

    # First, pull out all the <code></code> blocks, to keep them away
    # from Markdown (and preserve whitespace).
    #logger.info(content)
    print type(content)
    soup = BeautifulSoup(unicode(content))
    code_blocks = soup.findAll('code')
    new_tag = soup.new_tag('code')
    print "code_blcoks;::;:", code_blocks
    print "------------------------------------------------------------------------"
    #logger.info('code_blocks: %s' % code_blocks)
    for block in code_blocks:
        print block
        block.replaceWith(new_tag)

    print "------------------------------------------------------------------------"
    print "GAY!!!!!", soup
    print "------------------------------------------------------------------------"
    print "souyp fbd", soup.findAll('code')

    #for a in soup.findAll('a'):
    #    p = Tag(soup, 'p') #create a P element
    #    a.replaceWith(p)

    # Run the post through markdown.
    if safe == u"unsafe":
        safe_mode = False
    else:
        safe_mode = True

    #logger.info('soup code removed: %s' % soup)
    markeddown = markdown(unicode(soup), safe_mode=safe_mode)

    logger.info('Markdown: %s' % markeddown)
    #markeddown = '<h1 id="kas-dk-akkkk">kas;dk;akkkk</h1> <p><code class="removed"></code></p>'
    
    #markeddown = u'<code class="removed"></code>hdsfhs'
    # Replace the pulled code blocks with syntax-highlighted versions
    soup = BeautifulSoup(unicode(markeddown))
    #print soup

    empty_code_blocks, index = soup.findAll('code'), 0
    formatter = HtmlFormatter(cssclass='source')

    logger.info( "empty_code_blocks: %s %s %s" % (soup, empty_code_blocks, index))

    for empty_block in empty_code_blocks:
        #print "blcok", block, index
        language = ''
        if code_blocks[index].has_key(u'class'):
            # <code class='python'>python code</code>
            language = code_blocks[index][u'class'][0]
            logger.info('the language selected is %s' % language)
        #else:
        #    # <code>plain text, whitespace-preserved</code>
        #    language = u'text'
    
        #    print "language", language
        try:
            lexer = get_lexer_by_name(language, stripnl=True, encoding=u'UTF-8')
        except ClassNotFound:
            try:
                # Guess a lexer by the contents of the code_blocks[index].
                lexer = guess_lexer(code_blocks[index].renderContents())
                print "lexer", lexer, code_blocks[index].renderContents()
            except ClassNotFound:
                print "sceoncd valuevrror"
                # Just make it plain text.
                lexer = get_lexer_by_name(u'text', stripnl=True, encoding=u'UTF-8')

        #print "renderContents", (highlight(code_blocks[index].renderContents(), lexer, formatter))
        #empty_code_blocks[index].replaceWith(unicode(highlight(block.renderContents(), lexer, formatter)))
        #print highlight(code_blocks[index].renderContents(), lexer, formatter)
        new_tag = soup.new_tag("code")
        new_tag = BeautifulSoup(unicode(highlight(code_blocks[index].renderContents(), lexer, formatter)))
        empty_block.replaceWith(new_tag)#(highlight(code_blocks[index].renderContents(), lexer, formatter)))
        

        index = index + 1
        logger.info("empty_code_blocks: %s" % empty_code_blocks)
        #print soup
        #soup = soup.prettify()
        #print type(soup)
        #print unicode(soup)
        #print(soup.prettify(formatter="None"))
        #print dir(soup.prettify())
        #print soup.prettify(formatter="html")
        #print STYLE_MAP.keys()
    return soup


