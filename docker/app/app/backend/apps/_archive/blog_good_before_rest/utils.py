'''
    blog.utils
    ==========
'''
import logging
from markdown2 import markdown
# BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/
from bs4 import BeautifulSoup
# Pygments: http://pygments.org -- a generic syntax highlighter.
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound
# Get instance of logger
logger = logging.getLogger('project_logger')


def markup(content, safe=False):
    """ Takes content that assumed to be markdown converts to markup for beautiful html output.
        - Takes markdown content and converts it to markup.
        - Automatic code syntax highlighting for <code></code>
    """
    logger.info('markdown from utils.py')
    # Find all code blocks
    soup_mk = BeautifulSoup(unicode(content))
    code_blocks = soup_mk.findAll('code')
    # Remove code blocks
    for tag in code_blocks:
        tag.clear()

    markeddown = markdown(unicode(soup_mk), safe_mode=safe)
    soup_mk = BeautifulSoup(unicode(markeddown))

    code_blocks = soup_mk.findAll('code')
    soup = BeautifulSoup(unicode(content))
    code_tags = soup.findAll('code')
    formatter = HtmlFormatter()

    index = 0
    for tag in code_blocks:
        try:
            lexer = get_lexer_by_name(tag['class'][0])
            logger.info('lexer found by name: %s' % tag['class'][0])
        except (ClassNotFound, KeyError):
            logger.info('Attempting to guess lexer.')
            try:
                lexer = guess_lexer(tag.string)
                logger.info('lexer: %s' % lexer)
            except:
                logger.info('Setting to lexer to default.')
                lexer = get_lexer_by_name('text')  # default lexer

        new_tag = soup.new_tag("code")

        new_tag = BeautifulSoup(highlight(code_tags[index].string, lexer, formatter))
        tag.replaceWith(new_tag)
        index += 1

    return soup_mk
