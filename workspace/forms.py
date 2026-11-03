from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import DocumentShare


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            field: forms.TextInput(attrs={"class": "field"})
            for field in ("first_name", "last_name", "email")
        }


class ShareForm(forms.Form):
    username = forms.CharField(max_length=150)
    role = forms.ChoiceField(choices=DocumentShare.ROLE_CHOICES)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "field",
                "autocomplete": "email",
            }
        ),
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "field",
                "autocomplete": "given-name",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "field",
                "autocomplete": "family-name",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {
                "class": "field",
                "autocomplete": "username",
                "placeholder": "Choose a username",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "field",
                "autocomplete": "new-password",
                "placeholder": "Create a password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "field",
                "autocomplete": "new-password",
                "placeholder": "Confirm your password",
            }
        )
