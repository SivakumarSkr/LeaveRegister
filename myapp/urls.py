from django.urls import path

from myapp.views import active_report
from . import views

app_name = 'myapp'
urlpatterns = [
    path('leaverequest/', views.LeaveRequestCreate.as_view(), name='leaverequest'),
    path('', views.Home.as_view(), name='home'),
    path('leave-list', views.LeaveList.as_view(), name='leave-list'),
    path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
    path('wfh_create/', views.WorkFromHomeCreate.as_view(), name='wfh_create'),
    path('annual_leave/', views.AnnualLeaveList.as_view(), name='annual_leave'),
    path('leave_create/', active_report, name='active_leave'),
    path('home/', views.HomeForUser.as_view(), name='home2'),
]
