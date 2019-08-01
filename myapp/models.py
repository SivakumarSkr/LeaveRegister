import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group
from django.conf import settings

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField


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
    contact_number = PhoneNumberField()
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
        return self.leaverequest_set.all()

    def get_wfh_leaves(self):
        return self.workfromhome_set.set()

    @property
    def is_manager(self):
        return 'Manager' == self.groups.name


class AnnualLeaveDetails(models.Model):

    TOTAL_CASUAL_LEAVES = 12
    TOTAL_SICK_LEAVES = 12

    employee = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    year = models.PositiveIntegerField('Year', validators=[MaxValueValidator(2012), MinValueValidator(2050)])
    total_casual_leaves = models.PositiveSmallIntegerField(default=TOTAL_CASUAL_LEAVES)
    total_sick_leaves = models.PositiveSmallIntegerField(default=TOTAL_SICK_LEAVES)
    casual_leaves_used = models.PositiveSmallIntegerField(default=0)
    sick_leaves_used = models.PositiveSmallIntegerField(default=0)
    number_of_wfh_used = models.PositiveSmallIntegerField(default=0)

    def plus_sick_leave(self, number):
        self.sick_leaves_used += number
        self.save()

    def plus_casual_leave(self, number):
        self.casual_leaves_used += number
        self.save()

    def plus_work_from_home(self, number):
        self.number_of_wfh_used += number
        self.save()

    # def save(self, *args, **kwargs):
    #     if self.total_casual_leaves >= self.casual_leaves_used and self.total_sick_leaves >= self.sick_leaves_used:
    #         super(AnnualLeaveDetails, self).save(*args, **kwargs)


class Type(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    requested_date = models.DateField(auto_created=True)
    no_of_days = models.PositiveSmallIntegerField(default=1)
    from_date = models.DateField('From Date')
    to_date = models.DateField('To date')
    reason = models.TextField('Reason', max_length=500)
    is_approved = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def approve(self):
        self.is_approved = True
        self.save()


class LeaveRequest(Type):
    CASUAL = 'C'
    SICK = 'S'
    LEAVE_TYPE = (
        (CASUAL, 'Casual'),
        (SICK, 'Sick'),
    )
    leave_type = models.CharField('Leave Type', max_length=1, choices=LEAVE_TYPE)


class WorkFromHome(Type):
    pass
