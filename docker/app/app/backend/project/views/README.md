<a href="http://www.djangoproject.com/" ><img src="https://www.djangoproject.com/m/img/badges/djangoproject120x25.gif" border="0" alt="A Django project." title="A Django project." style="float: right;" /></a>

## 'views' Directory 

*(__Note__: This directory started as a port of [django-braces](https://github.com/brack3t/django-braces) therefore
you should periodically check the page for useful updates and ideas. )*

### Introduction
This is the views directory containing Django project wide configuration.

This should contain Reusable Class-based Views and useful functions when dealing with views.

e.g. ajax calls, extra status codes, permissions

### How to Use
- Decide which view you want for to forfill the role you require.
- Can the role be performed from a current mixin in mixins.py (See Below for a quick view of functionality)
    - If __yes__, use it by subclass it:

        *e.g.*

    ```Python
    class NewDetailView(AjaxResponseMixin, DetailView):
        model = Random
        ...
    ```
*(__Note__: mixin should always be first on the list of base classes.)*

    - If __no__, determine if the view is a one-off or it can be used as a reusable function/class. 
      Add to mixins.py if so and update README.md.

### Files

* README.md   - this file
* mixins.py   - this contains all of your reusable mixin views


### Main project wide views file - mixins.py
This file contains all useful functions and classes.


* __HttpResponseUnAuthorized__         - a extra status code HTTP response 401.
* __require_get__                      - requires/restricts to a GET ajax call.
* __require_post__                     - requires/restricts to a POST ajax call.
* __LoginRequiredMixin__               - a log in is required to view this page.
* __CsrfExemptMixin__                  - a view that exempts the CSRF requirements. __(Useful for debug)__
* __PermissionRequiredMixin__          - verifies that the logged in user has the correct permisson.
* __MultiplePermissionsRequiredMixin__ - verifies when multiple permissions are required.
* __SuperuserRequiredMixin__           - requires a user to be a superuser (is_superuser) to view the page.
* __StaffuserRequiredMixin__           - requires a user to be staff to view the page.
* __JSONResponseMixin__                - Allows easy serialization of simple data such as a dict or Django model/s.
* __AjaxResponseMixin__                - Handle ajax requests
* __PjaxResponseMixin__                - Handle pjax requests, essentially ajax with pushState(). Use if you want to handle normal responses as well as partial updates.

