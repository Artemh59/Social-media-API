from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class Post(models.Model):
    image = models.ImageField(null=True)
    text = models.TextField()


class Profile(models.Model):
    profile_picture = models.URLField(
        max_length=255,
        default="https://media.istockphoto.com/id/1354776457/vector/"
        "default-image-icon-vector-missing-picture-page-for-website-design-or-mobile-app-no-photo.jpg?"
        "s=612x612&w=0&k=20&c=w3OW0wX3LyiFRuDHo9A32Q0IUMtD4yjXEvQlqyYk9O4=",
    )
    bio = models.TextField()
    date_of_birth = models.DateField(null=True)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True
    )
    posts = models.ForeignKey(Post, related_name="profile", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Profile {self.user.username}"


class User(AbstractUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
