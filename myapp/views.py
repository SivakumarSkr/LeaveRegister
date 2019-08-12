from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, DetailView, RedirectView
from .models import LeaveRequest, WorkFromHome, AnnualLeaveDetail, current_year
from django.contrib.auth.decorators import user_passes_test, login_required;
from .forms import LeaveRequestForm, WorkFromHomeForm
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash, get_user_model, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
User = get_user_model()


class LeaveRequestCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'leave_creation_form.html'
    success_url = reverse_lazy('myapp:home')
    success_message = 'Your leave request was submitted'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.user = self.request.user
        model.annual_leave = self.request.user.current_year_detail()
        model.save()
        return super(LeaveRequestCreate, self).form_valid(form)


class Home(TemplateView):
    template_name = 'home.html'


class HomeForUser(TemplateView):
    template_name = 'home2.html'


class LeaveList(LoginRequiredMixin, ListView):
    model = LeaveRequest
    template_name = ['leavelist.html', ]
    context_object_name = 'leaves'

    def get_queryset(self):
        return self.request.user.get_leave_request().order_by('-requested_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        content = super(LeaveList, self).get_context_data(**kwargs)
        content['wfhs'] = self.request.user.get_wfh_leaves().order_by('-requested_date')
        return content


class WorkFromHomeCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = WorkFromHome
    template_name = 'work_from_home_create.html'
    form_class = WorkFromHomeForm
    success_message = 'Your work from home request is submitted'
    success_url = reverse_lazy('myapp:home')

    def form_valid(self, form):
        model = form.save(commit=False)
        model.user = self.request.user
        model.annual_leave = self.request.user.current_year_detail()
        model.save()
        return super(WorkFromHomeCreate, self).form_valid(form)


class Profile(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data()
        context['current_details'] = self.object.current_year_detail()
        return context


class ActivateReport(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        AnnualLeaveDetail.objects.create(
            user_profile=self.request.user,
            year=current_year(),
        )
        return redirect('myapp:profile', pk=self.request.user.pk)


@login_required
def active_report(request):
    AnnualLeaveDetail.objects.create(
        user_profile=request.user,
        year=current_year(),
    )
    return redirect('myapp:profile', pk=request.user.pk)


class AnnualLeaveList(LoginRequiredMixin, ListView):
    model = AnnualLeaveDetail
    template_name = 'annual_leave.html'

    def get_queryset(self):
        return self.request.user.annual_leaves.all()
