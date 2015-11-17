"""
    utils.py - a list of utility functions
"""
import logging
import hashlib
from difflib import get_close_matches
from sets import Set

from markdown2 import markdown
# BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/
from bs4 import BeautifulSoup
# Pygments: http://pygments.org -- a generic syntax highlighter.
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.util import ClassNotFound

#from .models import Comment

# Get instance of logger
logger = logging.getLogger('project_logger')

# HTML tags which comments, notes can be added against
# NOTE: No H1, H2, H3, H4. H5, H6  here
# If text is the same and commentable it may be hard to resync comments to it.
# H1 and H2 have a higher ability to be the same - lets reduce the risk by not making them commentable
COMMENTABLE_TAGS = ['p']


def calculate_id_name(message):
    """ Calculates hash value based on message. Useful for unique id - six hex characters.  6 digits - 16777216 permutations.
	TODO: check for hash collisions.
    """
    hash_object = hashlib.md5(b'%s'% message)
    return  hash_object.hexdigest()[0:5]

def find_all_commentable_tags(content):
    """ Finds all tags within html content which can be and returns a list of strings of the paragraphs. 
        TODO: if content is not <class 'bs4.BeautifulSoup'> or must be html
    """
    logger.debug('find_all_commentable_tags,')
    if isinstance(content, BeautifulSoup):
        contentSoup = content
    else:
        contentSoup = BeautifulSoup(unicode(content))

    p_tags = contentSoup.findAll(COMMENTABLE_TAGS)
    para_list = []
    for p_tag in p_tags:
        if p_tag.string is not None:
            para_list.append(p_tag.string)
    return para_list


def cwmarkdown(content, previous_content=None, post=None, comments=None, safe=False, preview_only=False):
    """ Codewheel's special markdown function. 
        - Takes markdown content and converts it to markup.
        - Automatic code syntax highlighting for <code></code>

        Updated Content - can invalidate comments. We have a best guess to try and keep comments but
                          may be wrong. It is a guess at best on trying to resync comments.

    """
    logger.info('cwmarkdown from utils.py')
    soup_mk = BeautifulSoup(unicode(content))
    code_blocks = soup_mk.findAll('code')

    for tag in code_blocks:
        tag.clear()

    print "mk", soup_mk
    markeddown = markdown(unicode(soup_mk), safe_mode=safe)
    soup_mk = BeautifulSoup(unicode(markeddown))
    code_blocks = soup_mk.findAll('code')
    print markeddown
    print "type of soup mk", type(soup_mk)

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
                lexer = guess_lexer(tag.string);  
                logger.info('lexer: %s' % lexer)
            except:
                logger.info('Setting to lexer to default.')
                lexer = get_lexer_by_name('text') # default lexer

        new_tag = soup.new_tag("code")

        new_tag = BeautifulSoup(highlight(code_tags[index].string, lexer, formatter))
        tag.replaceWith(new_tag)
        index += 1

    # The id name calculation is a hash function derived from text; if the text doesn't change the id shouldnt change.
    # Note however that it doesn't matter if it does because of the re-jig of ids
    # for the comments currently attached to the content (previous_content in this context)
    # If there is a hash collision in the content then we given it a overflow name plus an incrementing index
    p_tags = soup_mk.findAll(COMMENTABLE_TAGS)
    tag_index = 0
    for p_tag in p_tags:
        p_tag['id'] = calculate_id_name(str(tag_index) + str(p_tag))
        tag_index += 1




    # Resync of Ids with Comments that are attached to Post Object
    # TODO: If content hasn't changed and has comments attached we still replace with same ID -- this is inefficient and dangerous?
    # TODO: Add warning to the user that the comments had multiple matches and could be synced incorrectly.
    #       Ideally this could be shown under the editor.
    if previous_content:
        logger.info('previous_content found - Will need to resync any comments attached.')
        # Generate a list of the commentable text from the new content.
        new_commentable_tags = find_all_commentable_tags(str(soup_mk))
        # All idname in comments that current exist for this post.
        commentSet = Set([comment.idname for comment in comments.all()])
        logger.debug('There are %s comments current attached to this Post: %s' % (len(commentSet), commentSet))
        for idname in commentSet:

            find_text = BeautifulSoup(previous_content).find(id=idname)
            if find_text: 
                close_matches = get_close_matches(find_text.string, new_commentable_tags)
                # If match found replace id with old id
                # If no match is found the comment is no longer relevant and should be deleted.
                # Note: If more than one match is found we could run into problems. For now though, just log
                if close_matches:
                    if len(close_matches) > 1: 
                        logger.warn('There is more than one match in this post for text=%s.' % find_text)
                        logger.warn('We are going to guess its the one with the best match.')
                    logger.info('Close matches found - %s' % close_matches[0])
                    # Resync Comment to Content
                    for com in comments.all().filter(idname=idname):
                        # In preview mode, we don't want to change the database so modify content id instead.
                        if preview_only:
                            soup_mk.findAll(COMMENTABLE_TAGS, text=close_matches[0])[0]['id'] = idname
                        else:
                            com.idname = soup_mk.findAll(COMMENTABLE_TAGS, text=close_matches[0])[0]['id']
                            logger.info('Changed comment %s.id   ID to %s' % (com.id, com.idname))
                            com.save()
                else:
                    if not preview_only:
                        logger.info('No match found. This comment with idname %s is no longer relevant. Deleting Comments from post %s....' % (idname, post))
                        for com in comments.all().filter(idname=idname):
                            post.comments.remove(com)
            else:
                logger.error("There is a comment for this Post with idname=%s which cant be found in content. This shouldn't be possible. Something is wrong here... Out Of Sync?" % idname)



    return soup_mk



