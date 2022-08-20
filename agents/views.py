from urllib import request
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from leads.models import Agent
from .forms import AgentCreationForm
from django.urls import reverse


# Create your views here.

class AgentCreateView(CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentCreationForm

    def get_success_url(self):
        return reverse('agent_list')

    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.managed_by = self.request.user.userprofile  #assigning UserProfile object to manage_by managed_by == currently logged in user
        agent.save()
        return super(AgentCreateView, self).form_valid(form)

class AgentListView(ListView):
    template_name = 'agents/agent_list.html'
    def get_queryset(self):
        currently_logged_in_user = self.request.user.userprofile
        return Agent.objects.filter(managed_by = currently_logged_in_user)
    context_object_name = 'agents'

class AgentDetailView(DetailView):
    template_name = "agents/agent_detail.html"
    def get_queryset(self):
        currently_logged_in_user = self.request.user.userprofile
        return Agent.objects.filter(managed_by = currently_logged_in_user)
    context_object_name = 'agent'

class AgentUpdateView(UpdateView):
    template_name = 'agents/agent_update.html'
    context_object_name = 'agent'
    def get_queryset(self):
        currently_logged_in_user = self.request.user.userprofile
        return Agent.objects.filter(managed_by = currently_logged_in_user)
    form_class = AgentCreationForm

    def get_success_url(self):
        return reverse('agent_list')

class AgentDeleteView(DeleteView):
    template_name = 'agents/agent_delete.html'
    def get_queryset(self):
        currently_logged_in_user = self.request.user.userprofile
        return Agent.objects.filter(managed_by = currently_logged_in_user)

    def get_success_url(self):
        return reverse('agent_list')