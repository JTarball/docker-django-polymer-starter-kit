from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from apps.content.models import Post


# class AccountsUserCreationForm(forms.ModelForm):
#     """ A form for creating new users. Includes all the required fields, plus a repeated password.
#          View should have correct permissions.
#     """
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

#     class Meta:
#         model = AccountsUser
#         #fields = ('username', 'email', 'password1', 'password2')

#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             msg = "Passwords don't match"
#             raise forms.ValidationError(msg)
#         return password2

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(AccountsUserCreationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user


class PostChangeForm(forms.ModelForm):
    """ A form for updating users. Includes all the field on the user, but replaces the password field with admin's password hash display field. """

    class Meta:
        model = Post

    def form_valid(self, form):
        print "form_valid"
        return super(PostChangeForm, self).form_valid(form)

    def form_invalid(self, form):
        print "form_valid"
        return super(PostChangeForm, self).form_invalid(form)

    # def clean_email(self):
    #     print "cleaning email"
    #     email1 = self.cleaned_data.get("email")
    #     if email1 != "hello":
    #         msg = "Email don't match"
    #         raise forms.ValidationError(msg)
    #     return email1
    #def clean_title(self):
    #    print "cleaning email"
    #    return self.initial["title"]

    # def clean_password(self):
    #     """ Regardless of what the user provides, return the initial value. This is
    #         done her, rather than on the field, because the field does not have access
    #         to the initial value.
    #     """
    #     return self.initial["password"]
