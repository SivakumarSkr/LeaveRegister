from django import forms
from django.core.exceptions import ValidationError
from .models import LeaveRequest, WorkFromHome


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ('no_of_days', 'from_date', 'to_date', 'leave_type', 'reason')
        widgets = {'from_date': forms.TextInput(
            attrs={'type': 'date'}
        ),
            'to_date': forms.TextInput(
                attrs={'type': 'date'}
            ),
        }


class WorkFromHomeForm(forms.ModelForm):
    class Meta:
        model = WorkFromHome
        fields = ('no_of_days', 'from_date', 'to_date', 'reason')
        widgets = {'from_date': forms.TextInput(
            attrs={'type': 'date'}
        ),
            'to_date': forms.TextInput(
                attrs={'type': 'date'}
            ),
        }
    # def __init__(self, *args, **kwargs):
    # 	super(AddUserForm, self).__init__(*args, **kwargs)
    # 	self.fields['middle_name'].required = False


# class EditUserForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = (
#         'Employee_first_name', 'Middle_name', 'Employee_last_name', 'email', 'ph_no', 'emp_type', 'user_status')
#
#     # def clean_first_name(self):
#     # 	if self.cleaned_data["first_name"].strip() == '':
#     # 		raise ValidationError("First name is required.")
#     # 	return self.cleaned_data["first_name"]
#
#     # def clean_last_name(self):
#     # 	if self.cleaned_data["last_name"].strip() == '':
#     # 		raise ValidationError("Last name is required.")
#     # 	return self.cleaned_data["last_name"]
