This is the 'blog' app.

Create Simple Posts/Delete Posts for Superuser only. 
Integrates with 'search' app to give predictive search.


Dependencies
============
'search' App


Default Settings
=============


Install
=============

- add 'blog' to INSTALL_APPS in your django settings
- add blog app urls to your main urls.py
    from blog import urls as urls_blog
    url(r'^blog/', include(urls_blog)),