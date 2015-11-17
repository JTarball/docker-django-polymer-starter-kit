"""
    Form for PostCard
"""
from django import forms

from apps.content.models import PostCard


class PostCardForm(forms.ModelForm):
    """ A form for updating users. Includes all the field on the user, but replaces the password field with admin's password hash display field. """
    # Hide or Irrelevant Default Fields
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
    brokens = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
    likes_pretty = forms.CharField(widget=forms.HiddenInput(), required=False)
    views_pretty = forms.CharField(widget=forms.HiddenInput(), required=False)
    comments_pretty = forms.CharField(widget=forms.HiddenInput(), required=False)
    updated_at_pretty = forms.CharField(widget=forms.HiddenInput(), required=False)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = PostCard

    def form_valid(self, form):
        print "form_valid"
        return super(PostCardForm, self).form_valid(form)

    def form_invalid(self, form):
        print "form_valid"
        return super(PostCardForm, self).form_invalid(form)
