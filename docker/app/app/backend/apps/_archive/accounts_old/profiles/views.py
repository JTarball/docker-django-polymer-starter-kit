import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import CreateView, UpdateView, DetailView
from django.http import HttpResponse, HttpResponseBadRequest

from project.views.mixins import LoginRequiredMixin, SuperuserRequiredMixin, AjaxResponseMixin
from accounts.models import AccountsUser
from .forms import AccountsUserCreationForm, AccountsUserChangeForm


class AccountsCreateView(SuperuserRequiredMixin, CreateView):
    """ View for creating Account Users. You should be a superuser. """
    model = AccountsUser
    form_class = AccountsUserCreationForm
    template_name = 'accounts/profiles/backend_create_user.html'


class AccountsUpdateView(LoginRequiredMixin, UpdateView):
    """ View for updating Account User Information / Profile. """
    model = AccountsUser
    form_class = AccountsUserChangeForm
    template_name = 'accounts/profiles/backend_user.html'
    #name = 'accounts_change_user'


class AccountsUpdateModalView(LoginRequiredMixin, AjaxResponseMixin, UpdateView):
    """ View for updating Account User Information / Profile for Modal Page """
    model = AccountsUser
    template_name = 'accounts/profiles/backend_user_modal.html'
    context_object_name = 'post'
    # Technically not part of DetailView (part of updateview)
    form_class = AccountsUserChangeForm

        #self.object = Portfolios.objects.get(id=self.request.id)
        #form_class = self.get_form_class()
        #form = self.get_form(form_class)
        #context = self.get_context_data(object=self.object, form=form)
        #return self.render_to_response(context)
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context, ensure_ascii=False)
        print response_kwargs
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        print "form_invalid"
        response = super(AccountsUpdateModalView, self).form_invalid(form)
        if self.request.is_ajax():
            print "rendering to json response", form
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        print "form_valid"
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AccountsUpdateModalView, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response



    def get_ajax(self, request, *args, **kwargs):
        print "hjfdhskhfjkshhfjkshkdj"
        self.object = self.get_object()
        form = self.get_form(self.form_class)
        context = self.get_context_data(object=self.object, form=form)
        return render_to_response( 'accounts/profiles/backend_user_modal.html', context, 
                                       context_instance = RequestContext(request), mimetype='application/javascript')
