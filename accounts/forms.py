from django import forms
from accounts.models import AccountUser
from organizations.backends import invitation_backend
from organizations.backends.forms import UserRegistrationForm


class AccountUserForm(forms.ModelForm):
    """
    Form class for editing OrganizationUsers *and* the linked user model.
    """
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        exclude = ('user', 'is_admin')
        model = AccountUser

    def __init__(self, *args, **kwargs):
        super(AccountUserForm, self).__init__(*args, **kwargs)
        if self.instance.pk is not None:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        """
        This method saves changes to the linked user model.
        """
        if self.instance.pk is None:
            site = 'testing.com'
            self.instance.user = invitation_backend().invite_by_email(
                self.cleaned_data['email'],
                **{'first_name': self.cleaned_data['first_name'],
                   'last_name': self.cleaned_data['last_name'],
                   'organization': self.cleaned_data['organization'],
                   'domain': site})
        self.instance.user.first_name = self.cleaned_data['first_name']
        self.instance.user.last_name = self.cleaned_data['last_name']
        self.instance.user.email = self.cleaned_data['email']
        self.instance.user.save()
        return super(AccountUserForm, self).save(*args, **kwargs)


class RegistrationForm(UserRegistrationForm):
    """
    Form class that allows a user to register after clicking through an
    invitation.
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'disabled', 'readonly': 'readonly'}))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=128, widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password != password_confirm or not password:
            raise forms.ValidationError("Your password entries must match")
        return super(RegistrationForm, self).clean()
