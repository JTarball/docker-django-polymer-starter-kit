"""
    Form for Comment
"""
from django import forms

from blog.models import Comment


class CommentForm(forms.ModelForm):
    """ A form for updating users. Includes all the field on the user, but replaces the password field with admin's password hash display field. """
    # Hide Irrelevant Default Fields
    type = forms.IntegerField(widget=forms.HiddenInput(), initial=1, required=True)
    #likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
    #views = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
    #brokens = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
    #likes_pretty = forms.CharField(widget=forms.HiddenInput(), required=False)
    #views_pretty = forms.CharField(widget=forms.HiddenInput(), required=False)
    #comments_pretty = forms.CharField(widget=forms.HiddenInput(), required=False)
    #updated_at_pretty = forms.CharField(widget=forms.HiddenInput(), required=False)
    #slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ['content']

    def form_valid(self, form):
        print "form_valid"
        return super(CommentForm, self).form_valid(form)

    def form_invalid(self, form):
        print "form_valid"
        return super(CommentForm, self).form_invalid(form)










class StringListField(forms.CharField):
    def prepare_value(self, value):
    	print "prepare_value", value
        return ', '.join(value)
 
    def to_python(self, value):
        print "to_python StringListField", value
        if not value:
            return []
        
        return [item.strip() for item in value.split(',')]