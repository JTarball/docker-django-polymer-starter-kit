"""
Views which allow users to create and activate accounts.

"""
from django.views.generic import RedirectView
from django.shortcuts import redirect
from django.views.generic import CreateView, View
from django.http import HttpResponse

from project.views.mixins import AjaxResponseMixin, require_get, HttpResponseUnAuthorized
from .backend import AccountsBackend as backend

from .forms import RegistrationForm

from accounts.models import AccountsUser

class Activate(RedirectView):
    backend = backend()  # OPTIMISE: Outside of the class?

    def get_redirect_url(self, **kwargs):
        [activated, redirect_url] = self.backend.activate(**kwargs)  # activate
        return redirect_url






class Register(AjaxResponseMixin, RedirectView):
    """ Allows a user to register. """
    disallowed_url = 'registration_disallowed'

    def post(self, request, *args, **kwargs):
        # Registration Allowed?
        if not backend.registration_allowed: return redirect(self.disallowed_url)
        # Form Valid
        form = backend.form(data=request.POST, files=request.FILES)
        if form.is_valid():
            backend.register(request, **form.cleaned_data)  # register
            if self.kwargs.success_url is None:
                self.url = backend.post_registration_redirect
            else:
                self.url = self.kwargs.success_url  # successful redirect to successful url
        super(Activate, self).get()
        raise Exception('Your form is incorrect! %s ' % form.errors)  # FIXME: shouldnt have an exception here




class AccountsRegisterView(CreateView, RedirectView):
    """ View for creating Account Users. You should be a superuser. """
    model = AccountsUser
    form_class = RegistrationForm
    template_name = 'accounts/reg_form.html'
    success_url = 'complete'
    disallowed_url = 'registration_disallowed'
    
    def get_redirect_url(self, **kwargs):
        [activated, redirect_url] = self.backend.activate(**kwargs)  # activate
        return redirect_url


    def post(self, request, *args, **kwargs):
        # Override post has we shouldnt have a save in modelform 
        # 
        # Registration Allowed?
        if not backend.registration_allowed: return redirect(self.disallowed_url)
        # Form Valid
        form_class = self.get_form_class()
        print "GORM, ", form_class
        form = self.get_form(form_class)
        if form.is_valid():
            backend.register(request, **form.cleaned_data)  # register
            if self.kwargs.success_url is None:
                self.url = backend.post_registration_redirect
            else:
                self.url = self.kwargs.success_url  # successful redirect to successful url
        else:
            return self.form.form_invalid(form)

        #super(Activate, self).get()
        #raise Exception('Your form is incorrect! %s ' % form.errors)  # FIXME: shouldnt have an exception here  

    #form_class = self.get_form_class()
    #form = self.get_form(form_class)
    #if form.is_valid():
    #    return self.form_valid(form)
    #else:
    #    return self.form_invalid(form)


@require_get
class AjaxRestricted(AjaxResponseMixin, View):
    # A quick fire way to check if someone is logged in or not
    # returns a http status of 401 (Unauthorized) if not logged in
    # else return success 200 response
    def get_ajax(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseUnAuthorized('You are not logged in.')
        else:
            return HttpResponse('You are logged in.')


@require_get
class AjaxStaffRestricted(AjaxResponseMixin, View):
    # A quick fire way to check if someone is logged in or not
    # returns a http status of 401 (Unauthorized) if not logged in
    # else return success 200 response
    def get_ajax(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseUnAuthorized('You are not logged in.')
        else:
            return HttpResponse('You are have permisson.')






