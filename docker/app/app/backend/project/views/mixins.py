import warnings
import logging
import six

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.utils.http import urlquote
from django.views.generic import CreateView, View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response as render_to_resp
from django.template import RequestContext

# TODO write a doc for mixins?
import json
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db import models


from django.views.decorators.http import require_POST as post_only
from django.views.decorators.http import require_GET as get_only
 

from decorator import decorator

from django.http import Http404


def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError,\
        'Object of type %s with value of %s is not JSON serializable' % (
            type(obj), repr(obj)
            )


class JsonResponse(HttpResponse):
    """
    HttpResponse descendant, which return response with
    ``application/json`` mimetype.
    """

    def __init__(self, data, mimetype='application/json', status=200):
        super(JsonResponse, self).__init__(
            content=json.dumps(data, default=handler),
            mimetype=mimetype,
            status=status
        )

logger = logging.getLogger('project_logger')


# DECORATORS
def require_post(View):
    View.dispatch = method_decorator(post_only)(View.dispatch)
    return View

def require_get(View):
    View.dispatch = method_decorator(get_only)(View.dispatch)
    View.dispatch = method_decorator(ajax_required)(View.dispatch)
    return View


def ajax(login_required=False, require_GET=False, require_POST=False,
         require=None):
    """
    Usage:

    @ajax(login_required=True)
    def my_ajax_view(request):
        return {'count': 42}
    """

    def ajax(f, request, *args, **kwargs):
        """ wrapper function """
        if login_required:
            if not request.user.is_authenticated():
                return JsonResponse({
                    'status': 'error',
                    'error': 'Unauthorized',
                    }, status=401)

        # check request method
        method = None
        if require_GET:
            method = "GET"
        if require_POST:
            method = "POST"
        if require:
            method = require
        if method and method != request.method:
            return JsonResponse({
                'status': 'error',
                'error': 'Method not allowed',
                }, status=405)

        try:
            response = f(request, *args, **kwargs)
        except Http404:
            return JsonResponse({
                'status': 'error',
                'error': 'Not found',
            }, status=404)

        # check if it is an instance of HttpResponse
        # if hasattr(response, 'status_code'):
        #     status_code = response.status_code
        #     if status_code > 399:
        #         return JsonResponse({
        #                 'status': 'error',
        #                 'error': response.content,
        #             },
        #             status=status_code
        #         )


        #     return response

        # status_code = 200
        # if isinstance(response, tuple):
        #     response, status_code = response

        # return JsonResponse(response, status=status_code)

    return decorator(ajax)

def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """    
    def wrap(request, *args, **kwargs):
            logger.info("fdsfds")
            if not request.is_ajax():
                logger.info('The request was not ajax - not valid request.')
                return HttpResponseBadRequest()
            return f(request, *args, **kwargs)

    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return f





# Extra Status Codes
class HttpResponseUnAuthorized(HttpResponse):
    status_code = 401


class UserKwargModelFormMixin(object):
    """
    Generic model form mixin for popping user out of the kwargs and
    attaching it to the instance.

    This mixin must precede forms.ModelForm/forms.Form. The form is not
    expecting these kwargs to be passed in, so they must be popped off before
    anything else is done.
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # Pop the user off the
                                              # passed in kwargs.
        super(UserKwargModelFormMixin, self).__init__(*args, **kwargs)


class LoginRequiredMixin(object):
    """
    View mixin which verifies that the user has authenticated.

    NOTE: This should be the left-most mixin of a view.
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class CreateAndRedirectToEditView(CreateView):
    """
    Subclass of CreateView which redirects to the edit view.
    Requires property `success_url_name` to be set to a
    reversible url that uses the objects pk.
    """
    success_url_name = None

    def dispatch(self, request, *args, **kwargs):
        warnings.warn("CreateAndRedirectToEditView is deprecated and will be "
            "removed in a future release.", PendingDeprecationWarning)
        return super(CreateAndRedirectToEditView, self).dispatch(request,
            *args, **kwargs)

    def get_success_url(self):
        # First we check for a name to be provided on the view object.
        # If one is, we reverse it and finish running the method,
        # otherwise we raise a configuration error.
        if self.success_url_name:
            self.success_url = reverse(self.success_url_name,
                kwargs={'pk': self.object.pk})
            return super(CreateAndRedirectToEditView, self).get_success_url()

        raise ImproperlyConfigured(
            "No URL to reverse. Provide a success_url_name.")


class CsrfExemptMixin(object):
    """
    Exempts the view from CSRF requirements.

    NOTE:
        This should be the left-most mixin of a view.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(*args, **kwargs)


class PermissionRequiredMixin(object):
    """
    View mixin which verifies that the logged in user has the specified
    permission.

    Class Settings
    `permission_required` - the permission to check for.
    `login_url` - the login url of site
    `redirect_field_name` - defaults to "next"
    `raise_exception` - defaults to False - raise 403 if set to True

    Example Usage

        class SomeView(PermissionRequiredMixin, ListView):
            ...
            # required
            permission_required = "app.permission"

            # optional
            login_url = "/signup/"
            redirect_field_name = "hollaback"
            raise_exception = True
            ...
    """
    login_url = settings.LOGIN_URL  # LOGIN_URL from project settings
    permission_required = None  # Default required perms to none
    raise_exception = False  # Default whether to raise an exception to none
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth

    def dispatch(self, request, *args, **kwargs):
        # Make sure that a permission_required is set on the view,
        # and if it is, that it only has two parts (app.action_model)
        # or raise a configuration error.
        if self.permission_required == None or len(
            self.permission_required.split(".")) != 2:
            raise ImproperlyConfigured("'PermissionRequiredMixin' requires "
                "'permission_required' attribute to be set.")

        # Check to see if the request's user has the required permission.
        has_permission = request.user.has_perm(self.permission_required)

        if not has_permission:  # If the user lacks the permission
            if self.raise_exception:  # *and* if an exception was desired
                raise PermissionDenied  # return a forbidden response.
            else:
                return redirect_to_login(request.get_full_path(),
                                         self.login_url,
                                         self.redirect_field_name)

        return super(PermissionRequiredMixin, self).dispatch(request,
            *args, **kwargs)


class MultiplePermissionsRequiredMixin(object):
    """
    View mixin which allows you to specify two types of permission
    requirements. The `permissions` attribute must be a dict which
    specifies two keys, `all` and `any`. You can use either one on
    it's own or combine them. Both keys values are required be a list or
    tuple of permissions in the format of
    <app label>.<permission codename>

    By specifying the `all` key, the user must have all of
    the permissions in the passed in list.

    By specifying The `any` key , the user must have ONE of the set
    permissions in the list.

    Class Settings
        `permissions` - This is required to be a dict with one or both
            keys of `all` and/or `any` containing a list or tuple of
            permissions in the format of <app label>.<permission codename>
        `login_url` - the login url of site
        `redirect_field_name` - defaults to "next"
        `raise_exception` - defaults to False - raise 403 if set to True

    Example Usage
        class SomeView(MultiplePermissionsRequiredMixin, ListView):
            ...
            #required
            permissions = {
                "all": (blog.add_post, blog.change_post),
                "any": (blog.delete_post, user.change_user)
            }

            #optional
            login_url = "/signup/"
            redirect_field_name = "hollaback"
            raise_exception = True
    """
    login_url = settings.LOGIN_URL  # LOGIN_URL from project settings
    permissions = None  # Default required perms to none
    raise_exception = False  # Default whether to raise an exception to none
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth

    def dispatch(self, request, *args, **kwargs):
        print "dispatch", self.raise_exception
        self._check_permissions_attr()

        perms_all = self.permissions.get('all') or None
        perms_any = self.permissions.get('any') or None

        self._check_permissions_keys_set(perms_all, perms_any)
        self._check_perms_keys("all", perms_all)
        self._check_perms_keys("any", perms_any)

        # If perms_all, check that user has all permissions in the list/tuple
        if perms_all:
            print "perms", perms_all, request.user.has_perms(perms_all)

            if not request.user.has_perms(perms_all):
                if self.raise_exception:
                    raise PermissionDenied
                return redirect_to_login(request.get_full_path(),
                                         self.login_url,
                                         self.redirect_field_name)

        # If perms_any, check that user has at least one in the list/tuple
        if perms_any:
            has_one_perm = False
            for perm in perms_any:
                if request.user.has_perm(perm):
                    has_one_perm = True
                    break

            if not has_one_perm:
                if self.raise_exception:
                    raise PermissionDenied
                return redirect_to_login(request.get_full_path(),
                                         self.login_url,
                                         self.redirect_field_name)

        return super(MultiplePermissionsRequiredMixin, self).dispatch(request,
            *args, **kwargs)

    def _check_permissions_attr(self):
        """
        Check permissions attribute is set and that it is a dict.
        """
        if self.permissions is None or not isinstance(self.permissions, dict):
            raise ImproperlyConfigured("'PermissionsRequiredMixin' requires "
                "'permissions' attribute to be set to a dict.")

    def _check_permissions_keys_set(self, perms_all=None, perms_any=None):
        """
        Check to make sure the keys `any` or `all` are not both blank.
        If both are blank either an empty dict came in or the wrong keys
        came in. Both are invalid and should raise an exception.
        """
        if perms_all is None and perms_any is None:
            raise ImproperlyConfigured("'PermissionsRequiredMixin' requires"
                "'permissions' attribute to be set to a dict and the 'any' "
                "or 'all' key to be set.")

    def _check_perms_keys(self, key=None, perms=None):
        """
        If the permissions list/tuple passed in is set, check to make
        sure that it is of the type list or tuple.
        """
        if perms and not isinstance(perms, (list, tuple)):
            raise ImproperlyConfigured("'MultiplePermissionsRequiredMixin' "
                "requires permissions dict '%s' value to be a list "
                "or tuple." % key)


class UserFormKwargsMixin(object):
    """
    CBV mixin which puts the user from the request into the form kwargs.
    Note: Using this mixin requires you to pop the `user` kwarg
    out of the dict in the super of your form's `__init__`.
    """
    def get_form_kwargs(self):
        kwargs = super(UserFormKwargsMixin, self).get_form_kwargs()
        # Update the existing form kwargs dict with the request's user.
        kwargs.update({"user": self.request.user})
        return kwargs


class SuperuserRequiredMixin(object):
    """
    Mixin allows you to require a user with `is_superuser` set to True.
    """
    login_url = settings.LOGIN_URL  # LOGIN_URL from project settings
    raise_exception = False  # Default whether to raise an exception to none
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:  # If the user is a standard user,
            if self.raise_exception:  # *and* if an exception was desired
                raise PermissionDenied  # return a forbidden response.
            else:
                return redirect_to_login(request.get_full_path(),
                                         self.login_url,
                                         self.redirect_field_name)

        return super(SuperuserRequiredMixin, self).dispatch(request,
            *args, **kwargs)


class StaffuserRequiredMixin(object):
    """
    Mixin allows you to require a user with `is_staff` set to True.
    """
    login_url = settings.LOGIN_REDIRECT_URL  # LOGIN_URL from project settings
    raise_exception = False  # Default whether to raise an exception to none
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:  # If the request's user is not staff,
            if self.raise_exception:  # *and* if an exception was desired
                raise PermissionDenied  # return a forbidden response
            else:
                return redirect_to_login(request.get_full_path(),
                                         self.login_url,
                                         self.redirect_field_name)

        return super(StaffuserRequiredMixin, self).dispatch(request,
            *args, **kwargs)


class JSONResponseMixin(object):
    """
    A mixin that allows you to easily serialize simple data such as a dict or
    Django models.
    """
    content_type = None
    json_dumps_kwargs = None
    json_encoder_class = DjangoJSONEncoder

    def get_content_type(self):
        if (self.content_type is not None and
            not isinstance(self.content_type,
                           (six.string_types, six.text_type))):
            raise ImproperlyConfigured(
                '{0} is missing a content type. Define {0}.content_type, '
                'or override {0}.get_content_type().'.format(
                    self.__class__.__name__))
        return self.content_type or "application/json"

    def get_json_dumps_kwargs(self):
        if self.json_dumps_kwargs is None:
            self.json_dumps_kwargs = {}
        self.json_dumps_kwargs.setdefault('ensure_ascii', False)
        return self.json_dumps_kwargs

    def render_json_response(self, context_dict, status=200):
        """
        Limited serialization for shipping plain data. Do not use for models
        or other complex or custom objects.
        """
        json_context = json.dumps(
            context_dict,
            cls=self.json_encoder_class,
            **self.get_json_dumps_kwargs()).encode('utf-8')
        return HttpResponse(json_context,
                            content_type=self.get_content_type(),
                            status=status)

    def render_json_object_response(self, objects, **kwargs):
        """
        Serializes objects using Django's builtin JSON serializer. Additional
        kwargs can be used the same way for django.core.serializers.serialize.
        """
        # Serializers - serialize is only meant for querysets
        json_data = serializers.serialize("json", objects, **kwargs)
        return HttpResponse(json_data, content_type=self.get_content_type())

    def render_json_form_response(self, context_dict):
        """ This method serialises a Django form and
        returns JSON object with its fields and errors

        {
          fields: {
            message: 'content of message field',
          },
          errors: {
            non_field_errors: 'errors that are not correspond to any particular field',
            fields: {
              message: 'errors related to message field'
            }
          }
          options: { },   // additional data that we want to return to the client
          success: false  // or true if the form is valid
        }

        """
        logger.info("%s" % context_dict)
        form = context_dict.get('form')

        json_data = json.dumps(context_dict, cls=DjangoJSONEncoder)
        return HttpResponse(json_data,
                            content_type=self.get_content_type(),
                            status=200)



        to_json = {}
        options = context_dict.get('options', {})
        to_json.update(options=options)
        to_json.update(success=context_dict.get('success', False))
        fields = {}
        for field_name, field in form.fields.items():
            if isinstance(field, models.DateField) and isinstance(form[field_name].value(), models.DateField.date):
                fields[field_name] = unicode(form[field_name].value().strftime('%d.%m.%Y'))
            else:
                fields[field_name] = form[field_name].value() and unicode(form[field_name].value()) or form[field_name].value()
        to_json.update(fields=fields)
        if form.errors:
            errors = {
                'non_field_errors': form.non_field_errors(),
            }
            fields = {}
            for field_name, text in form.errors.items():
                fields[field_name] = text
            errors.update(fields=fields)
            to_json.update(errors=errors)
        #return json.dumps(to_json)
        return HttpResponse(json.dumps(to_json),
                            content_type=self.get_content_type(),
                            status=200)




# class JSONFormResponseMixin(object):
#     """

#     """
#     def render_to_response(self, context, **httpresponse_kwargs):
#         return self.get_json_response(
#             self.convert_context_to_json(context),
#             **httpresponse_kwargs
#         )
#     def get_json_response(self, content, **httpresponse_kwargs):
#         return HttpResponse(
#             content,
#             content_type='application/json',
#             **httpresponse_kwargs
#         )
#     def convert_context_to_json(self, context):
#         u""" This method serialises a Django form and
#         returns JSON object with its fields and errors
#         """
#         form = context.get('form')
#         to_json = {}
#         options = context.get('options', {})
#         to_json.update(options=options)
#         to_json.update(success=context.get('success', False))
#         fields = {}
#         for field_name, field in form.fields.items():
#             if isinstance(field, DateField) \
#                     and isinstance(form[field_name].value(), datetime.date):
#                 fields[field_name] = \
#                     unicode(form[field_name].value().strftime('%d.%m.%Y'))
#             else:
#                 fields[field_name] = \
#                     form[field_name].value() \
#                     and unicode(form[field_name].value()) \
#                     or form[field_name].value()
#         to_json.update(fields=fields)
#         if form.errors:
#             errors = {
#                 'non_field_errors': form.non_field_errors(),
#             }
#             fields = {}
#             for field_name, text in form.errors.items():
#                 fields[field_name] = text
#             errors.update(fields=fields)
#             to_json.update(errors=errors)
#         return json.dumps(to_json)


class AjaxResponseMixin(object):
    """
    Mixin allows you to define alternative methods for ajax requests. Similar
    to the normal get, post, and put methods, you can use get_ajax, post_ajax,
    and put_ajax.
    """

    def dispatch(self, request, *args, **kwargs):
        logger.error("AjaxResponseMixin, dispatch method %s" % request.is_ajax())
        request_method = request.method.lower()

        if request.is_ajax() and request_method in self.http_method_names:
            handler = getattr(self, "{0}_ajax".format(request_method),
                              self.http_method_not_allowed)
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return handler(request, *args, **kwargs)

        return super(AjaxResponseMixin, self).dispatch(
            request, *args, **kwargs)

    def get_ajax(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def post_ajax(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def put_ajax(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def delete_ajax(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


# Abstract Class
# TODO: explanation needed about this classes and how they relate to the url
# ----------------------------------------------------------------------------
class PjaxResponseMixin(AjaxResponseMixin):
    pjax_template_name = ''      # This is the html template for the pjax response (html for partial update)

    def get(self, request, *args, **kwargs):
        logger.info('PjaxResponseMixin, this is the get function called from %s' % self.__class__.__name__ )
        self.request = request   # Used in response_to_response
        return super(PjaxResponseMixin, self).get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        logger.info('PjaxResponseMixin, this is the get_context_data function call.')
        context = super(PjaxResponseMixin, self).get_context_data(**kwargs)
        return context

    def render_to_response(self, context):
        """ Override render_to_response of view - if ajax then update pjax style! else normal render response."""
        logger.info('PjaxResponseMixin, this is the render_to_response function call. The context: %s' % context)
        if self.request.is_ajax():
            logger.info('PjaxResponseMixin, this is a ajax request')
            return render_to_resp( self.pjax_template_name, context, context_instance = RequestContext(self.request, { 'pjax': self.request.META.get('HTTP_X_PJAX'),}), content_type='application/javascript')
        else:
            logger.info('PjaxResponseMixin, this is a normal request')
            return super(PjaxResponseMixin, self).render_to_response(context)





class AjaxOnlyResponseMixin(AjaxResponseMixin):
    """
    Mixin allows you to define alternative methods for ajax requests. Similar
    to the normal get, post, and put methods, you can use get_ajax, post_ajax,
    and put_ajax.
    """

    def dispatch(self, request, *args, **kwargs):
        logger.info("AjaxResponseMixin, dispatch method %s %s" % (request.is_ajax(), request.method.lower()))
        request_method = request.method.lower()

        if request.is_ajax() and request_method in self.http_method_names:
            handler = getattr(self, "{0}_ajax".format(request_method),
                              self.http_method_not_allowed)
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return handler(request, *args, **kwargs)
        else:
            logger.error("AjaxResponseMixin,  bad request %s" % request.is_ajax())
            raise PermissionDenied


class AjaxOnlyAPIView(JSONResponseMixin, AjaxOnlyResponseMixin, View):

    def get_ajax(self, request, *args, **kwargs):
        logger.info("%s, get_ajax (%s)" % (self.__class__.__name__, request.path))
        self.object = self.get_object()
        return self.render_json_object_response([self.object])


class AjaxOnlyAPIDetailView(JSONResponseMixin, AjaxOnlyResponseMixin, DetailView):

    def get_ajax(self, request, *args, **kwargs):
        logger.info("%s, get_ajax (%s)" % (self.__class__.__name__, request.path))
        self.object = self.get_object()
        return self.render_json_object_response([self.object])


class AjaxOnlyAPIListView(JSONResponseMixin, AjaxOnlyResponseMixin, ListView):

    def get_ajax(self, request, *args, **kwargs):
        logger.info("%s, get_ajax (%s)" % (self.__class__.__name__, request.path))
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_paginate_by(self.object_list) is not None
                    and hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.")
                        % {'class_name': self.__class__.__name__})
        context = self.get_context_data()
        return self.render_json_object_response(self.object_list)


class AjaxOnlyAPICreateView(JSONResponseMixin, AjaxOnlyResponseMixin, CreateView):

    def get_ajax(self, request, *args, **kwargs):
        logger.info("%s, get_ajax (%s)" % (self.__class__.__name__, request.path))
        form = self.get_form()
        self.object = None
        return self.render_json_form_response(self.get_context_data(form=form))
