from django.urls import path
from . import views


app_name = 'myapp'
urlpatterns = [
	path('leaverequest/', views.LeaveRequestCreate.as_view(), name='leaverequest'),
	path('', views.Home.as_view(), name='home'),
	# path('addUser', views.add_user, name='add_user'),
	# path('editUser', views.edit_user, name='edit_user'),
	# path('edituser', views.edit_user_1, name='edit_user_1'),
	# path('mapUser', views.map_user, name='map_user'),
	# path('leaveRequest', views.leave_request, name='leave_request'),
	# path('leaveHistory', views.history, name='history'),
	# path('managerHistory', views.mng_history, name='mng_history'),
	# path('PendingRequests', views.pending, name='pending'),
	# path('teamHistory', views.team_history, name='team_history'),
	# path('teamHistory_1', views.team_history_1, name='team_history_1'),
	# path('userHistory', views.user_history, name='user_history'),
	# path('changePassword', views.change_password, name='change_password'),
	# path('editHistory', views.edit_history, name='edit_history'),
]
