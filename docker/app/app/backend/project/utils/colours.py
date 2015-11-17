#!/usr/bin/env python
"""
    utils.colours
    -------------

    Colour Utility

"""
import sys
import subprocess

if sys.version_info >= (2,7):
    from subprocess import check_output as check_cmd
elif sys.version_info >= (2.5):
    from subprocess import check_call as check_cmd
else: 
    raise ImportError('Python Version is not compatible')



#--------------------------------------------------------------------------------------------

class ColourCodes(object):
    """
    Provides ANSI terminal color codes which are gathered via the ``tput``
    utility. That way, they are portable. If there occurs any error with
    ``tput``, all codes are initialized as an empty string.
 
    The provides fields are listed below.
 
    Control: reset / reset_underline / reset_standout
 
    Special : underline / standout / rev / bold
 
    Colors: red / green / yellow / blue / purple / cyan / white / grey

    Light Colours: light_blue / light_yellow / light_green / light_purple

    Strong Colours: strong_red / strong_green / strong_yellow / strong_blue / strong_purple / strong_orange

    Background Colours: bg_blue / bg_grey
 
    """
    def __init__(self):
        try:
            self.bold = check_cmd("tput bold".split())
            self.rev = check_cmd("tput sgr0".split())
            self.standout = check_cmd("tput smso".split())
            self.reset_standout = check_cmd("tput rmso".split())
            self.underline = check_cmd("tput smul".split())
            self.reset_underline = check_cmd("tput rmul".split())
            self.reset = check_cmd("tput sgr0".split())

            self.red = check_cmd("tput setaf 1".split())
            self.green = check_cmd("tput setaf 2".split())
            self.yellow = check_cmd("tput setaf 3".split())
            self.blue = check_cmd("tput setaf 4".split())
            self.purple = check_cmd("tput setaf 5".split())
            self.cyan = check_cmd("tput setaf 6".split())
            self.white = check_cmd("tput setaf 7".split())
            self.grey = check_cmd("tput setaf 8".split())

            self.light_blue = check_cmd("tput setaf 69".split())
            self.light_yellow = check_cmd("tput setaf 228".split())
            self.light_green = check_cmd("tput setaf 43".split())
            self.light_purple = check_cmd("tput setaf 99".split())

            self.strong_red = check_cmd("tput setaf 160".split())  
            self.strong_green = check_cmd("tput setaf 34".split())
            self.strong_yellow = check_cmd("tput setaf 226".split())
            self.strong_blue = check_cmd("tput setaf 21".split())
            self.strong_purple = check_cmd("tput setaf 57".split())
            self.strong_orange = check_cmd("tput setaf 202".split())

            self.bg_blue = check_cmd("tput setab 32".split())
            self.bg_grey = check_cmd("tput setab 248".split())

        except subprocess.CalledProcessError as e:
            self.bold = ""
            self.rev = ""
            self.standout = ""
            self.reset_standout = ""
            self.underline = ""
            self.reset_underline = ""
            self.reset = ""

            self.red = ""
            self.green = ""
            self.yellow = ""
            self.blue = ""
            self.purple = ""
            self.cyan = ""
            self.white = ""
            self.grey = ""

            self.light_blue = ""
            self.light_yellow = ""
            self.light_green = ""
            self.light_purple = ""

            self.strong_red = ""
            self.strong_green = ""
            self.strong_yellow = ""
            self.strong_blue = ""
            self.strong_purple = ""
            self.strong_orange = ""

            self.background_blue = ""
            self.background_grey = ""

_c = ColourCodes()


#-----------------------------------------------------------------------------
def colourise(msg='', colour=_c.green):
    return colour + msg + _c.reset
#-----------------------------------------------------------------------------------
# HELPER FUNCTION -- need to stick them below _c bit
def bold(msg): return colourise(msg, _c.bold)
def rev(msg): return colourise(msg, _c.rev)
def standout(msg): return colourise(msg, _c.standout)
def underline(msg): return colourise(msg, _c.underline)

def red(msg): return colourise(msg, _c.red)
def green(msg): return colourise(msg, _c.green)
def yellow(msg): return colourise(msg, _c.yellow)
def blue(msg): return colourise(msg, _c.blue)
def purple(msg): return colourise(msg, _c.purple)
def cyan(msg): return colourise(msg, _c.cyan)
def white(msg): return colourise(msg, _c.white)
def grey(msg): return colourise(msg, _c.grey)

def lblue(msg): return colourise(msg, _c.light_blue)
def lyellow(msg): return colourise(msg, _c.light_yellow)
def lgreen(msg): return colourise(msg, _c.light_green)
def lpurple(msg): return colourise(msg, _c.light_purple)

def sred(msg): return colourise(msg, _c.strong_red)
def sgreen(msg): return colourise(msg, _c.strong_green)
def syellow(msg): return colourise(msg, _c.strong_yellow)
def sblue(msg): return colourise(msg, _c.strong_blue)
def spurple(msg): return colourise(msg, _c.strong_purple)
def sorange(msg): return colourise(msg, _c.strong_orange)

def bgblue(msg): return colourise(msg, _c.bg_blue)
def bggrey(msg): return colourise(msg, _c.bg_grey)