"""
    blog.forms.forms
    ================

    Forms for Blog App - Creating/Updating
"""
from django import forms

from blog.models import Post


class PostCreateForm(forms.ModelForm):
    """ A form for create a Blog Post. """
    class Meta:
        model = Post
        fields = ['title', 'tags', 'content']
