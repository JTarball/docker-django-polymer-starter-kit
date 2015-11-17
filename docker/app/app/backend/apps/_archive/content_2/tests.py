"""
# ============================================================================ #
# tests.py
# 
# Author : Danvir Guram
# Date   : 25/6/2012
#
# Test Based on django-whatever (using the standard unittest module)
#
# NOTE : run "manage.py test"
#
# ============================================================================ #
"""
#user = any_model(Root)
from django.test import TestCase
from django_any import any_model
from django_any.test import WithTestDataSeed

from models import *  # To make the content app more generic (load all models)


class TestContent(TestCase):
    """ A class to test the Content App. """
    __metaclass__ = WithTestDataSeed


    def pages(self):
    	"""
    	Tests all the page url: based on url <root>/<category>/<subcategory>/<slug>
    	"""

        for root_cat in Root.get.objects.get.all():
        	for cat_cat in Category.get.objects.get.all():
        		for cat_subcat in subcat:
        			for cat_slug in slug:
        				print "poo"




    def test_Root(self):
        """
        Tests that 1 + 1 always equalsss 2.
        """
        #print self
        #print dir(self)
        #print self.__class__.__doc__
        #print dir(self.test_Root.__str__)
        #print self.__call__.__doc__
        #print dir(self.test_Root.__func__)
        print self.test_Root.__doc__
        print self.test_Root.__format__
        print dir(self.test_Root)

        #print self.test_Root.__name__

        user = any_model(Root)


        self.assertEqual(1 + 1, 2)


# test all pages
# when debug off 404
# only get one result for a page
#




# ============================================================================ #
# EOF                                                                          #
# ============================================================================ #