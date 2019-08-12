from rest_framework import serializers
from .models import LeaveRequest, WorkFromHome, UserProfile


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = [
            'user',
            'no_of_days',
            'from_date',
            'to_date',
            'reason',
            'leave_type',
        ]
        extra_kwargs = {
            'is_approved': {
                'read_only': True,
            },
            'user': {
                'read_only': True,
            },

        }


class WFHRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkFromHome
        fields = [
            'user',
            'no_of_days',
            'from_date',
            'to_date',
            'reason',
        ]
        extra_kwargs = {
            'user': {
                'read_only': True,
            },
            'is_approved': {
                'read_only': True,
            }
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'middle_name', 'last_name', 'contact_number',
                  'image', 'groups', 'department_name', 'designation', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }
