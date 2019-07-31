from django.contrib import admin
from django.forms import ModelForm
from django.conf import settings
from .models import UserProfile, Department, LeaveRequest


# Register your models here.

class DepartmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)

        self.fields['manager'].queryset = UserProfile.objects.filter(groups__name='Managers')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    form = DepartmentForm


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_active', 'department_name', 'groups', 'is_superuser')
    exclude = ('user_permissions', )
    readonly_fields = ('last_login',)


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    date_hierarchy = 'requested_date'
