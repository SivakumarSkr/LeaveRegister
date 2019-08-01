from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView, TemplateView, ListView, DetailView

from .models import LeaveRequest, WorkFromHome
from django.contrib.auth.decorators import user_passes_test, login_required;
from .forms import LeaveRequestForm, WorkFromHomeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.http import HttpResponse

User = get_user_model()


class LeaveRequestCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'leave_creation_form.html'
    success_url = 'myapp:home'
    success_message = 'Your leave request was submitted'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.user = self.request.user
        model.save()


class Home(TemplateView):
    template_name = 'home.html'


class LeaveList(LoginRequiredMixin, ListView):
    model = LeaveRequest
    template_name = 'leavelist.html'
    paginate_by = 10
    context_object_name = 'leaves'

    def get_queryset(self):
        return self.request.user.get_leave_request()

    def get_context_data(self, *, object_list=None, **kwargs):
        content = super(LeaveList, self).get_context_data(**kwargs)
        content['wfh'] = self.request.user.get_wfh_leaves()
        return content


class WorkFromHomeCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = WorkFromHome
    template_name = 'work_from_home_create.html'
    form_class = WorkFromHomeForm
    success_message = 'Your work from home request is submitted'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.user = self.request.user
        model.save()


class Profile(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['leave_details'] = self.object.annualleavedetails
        return context

