import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group
from django.conf import settings

# Create your models here.


class Department(models.Model):
    name = models.CharField('Name', max_length=30)
    manager = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=20)
    middle_name = models.CharField('middle name', max_length=20, blank=True)
    last_name = models.CharField('last name', max_length=20, blank=True)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, verbose_name='Employee Type')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='users', null=True,
                                        blank=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.get_full_name()

    def get_leave_request(self):
        return self.leaverequests.all()

    def get_approved_leaves(self):
        return self.leaverequests.filter(is_approved=True)

    @property
    def is_manager(self):
        return 'Manager' == self.groups.name


class LeaveRequest(models.Model):
    CASUAL = 'C'
    SICK = 'S'
    OTHER = 'O'
    LEAVE_TYPE = (
        (CASUAL, 'Casual'),
        (SICK, 'Sick'),
        (OTHER, 'Other')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leaverequests')
    requested_date = models.DateField(auto_created=True)
    from_date = models.DateField('From Date')
    to_date = models.DateField('To date')
    leave_type = models.CharField('Leave Type', max_length=10, choices=LEAVE_TYPE)
    reason = models.TextField('Reason', max_length=500)
    is_approved = models.BooleanField(default=False)
