from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

from .models import Gender
from .models import Specialty
from .models import User
from .models import UserRoles


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.AdminUserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    name = forms.CharField(max_length=150)

    role = forms.ChoiceField(
        choices=UserRoles.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
        label=_("Role"),
        help_text=_("Select your role"),
    )

    gender = forms.ChoiceField(
        choices=Gender.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
        label=_("Gender"),
        help_text=_("Select your gender"),
    )

    specialty = forms.ChoiceField(
        choices=Specialty.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
        label=_("Specialty"),
        help_text=_("Select your specialty"),
    )

    def save(self, request):
        user = super().save(request)
        user.name = self.cleaned_data["name"]
        user.role = self.cleaned_data["role"]
        user.gender = self.cleaned_data["gender"]
        user.specialty = self.cleaned_data["specialty"]
        user.save()
        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """

    name = forms.CharField(max_length=150)

    role = forms.ChoiceField(
        choices=UserRoles.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
        label=_("Role"),
        help_text=_("Select your role"),
    )

    gender = forms.ChoiceField(
        choices=Gender.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
        label=_("Gender"),
        help_text=_("Select your gender"),
    )

    specialty = forms.ChoiceField(
        choices=Specialty.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
        label=_("Specialty"),
        help_text=_("Select your specialty"),
    )

    def save(self, request):
        user = super().save(request)
        user.name = self.cleaned_data["name"]
        user.role = self.cleaned_data["role"]
        user.gender = self.cleaned_data["gender"]
        user.specialty = self.cleaned_data["specialty"]
        user.save()
        return user
