from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.db.models import TextChoices
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class UserRoles(TextChoices):
    ADMIN = "admin", _("Admin")
    CLIENT = "client", _("Client")
    WORKER = "worker", _("Worker")


class RegistrationRoles(TextChoices):
    CLIENT = "client", _("Client")
    WORKER = "worker", _("Worker")


class Gender(TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")


class Specialty(TextChoices):
    DEVELOPER = "developer", _("Developer")
    DESIGNER = "designer", _("Designer")
    MANAGER = "manager", _("Manager")
    OTHER = "other", _("Other")


class User(AbstractUser):
    """
    Default custom user model for Order API.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)

    role = CharField(  # noqa: DJ001
        _("Role"),
        null=True,
        blank=False,
        max_length=20,
        choices=UserRoles.choices,
    )

    gender = CharField(  # noqa: DJ001
        _("Gender"),
        max_length=10,
        choices=Gender.choices,
        null=True,
        blank=False,
    )

    specialty = CharField(  # noqa: DJ001
        _("Specialty"),
        max_length=20,
        choices=Specialty.choices,
        null=True,
        blank=True,
    )

    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
