'''
    blog.utils
    ==========

'''
from markdown2 import markdown
# BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/
from bs4 import BeautifulSoup


def markup(markdown):
    """ Takes content that assumed to be markdown converts to markup for beautiful html output. """
