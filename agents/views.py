import random
from django.core.mail import send_mail
from django.shortcuts import render
from .mixins import ManagementAndLoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView,FormView

from leads.models import Agent, Lead
from .forms import AgentCreationForm, AssignAgentForm
from django.urls import reverse


# Create your views here.

# we created ManagementAndLoginRequiredMixin 
# for the purpose of restricting the currently logged in user 
# who might be an  agent from accessing anything relating to the management

class AgentCreateView(ManagementAndLoginRequiredMixin, CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentCreationForm

    def get_success_url(self):
        return reverse('agent_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_management = False
        user.set_password(f'{random.randint(1,100000)}')
        user.save()

        Agent.objects.create(user=user, managed_by = self.request.user.userprofile)
        # managed by above means the agent is managed by the user creating it

        send_mail(
            'Invitation to be an Agent.',
            'You have been invited to be an agent at djcrm. To start working, visit our site to reset your password and login. Thank you',
            from_email='fashinaoluwaseun36@gmail.com',
            recipient_list=[user.email],
        )
        return super(AgentCreateView, self).form_valid(form)

# our logged_in_management here in the views refer to the currently logged in management
# and we want to filter based on the agent specific for each managements

class AgentListView(ManagementAndLoginRequiredMixin, ListView):
    template_name = 'agents/agent_list.html'
    def get_queryset(self):
        logged_in_management = self.request.user.userprofile
        return Agent.objects.filter(managed_by = logged_in_management)
    context_object_name = 'agents'

class AgentDetailView(ManagementAndLoginRequiredMixin, DetailView):
    template_name = "agents/agent_detail.html"
    def get_queryset(self):
        logged_in_management = self.request.user.userprofile
        return Agent.objects.filter(managed_by = logged_in_management)
    context_object_name = 'agent'

class AgentUpdateView(ManagementAndLoginRequiredMixin, UpdateView):
    form_class = AgentCreationForm
    template_name = 'agents/agent_update.html'

    def get_queryset(self):
        logged_in_management = self.request.user.userprofile
        return Agent.objects.filter(managed_by = logged_in_management)

    def get_success_url(self):
        return reverse('agent_list')

class AgentDeleteView(ManagementAndLoginRequiredMixin, DeleteView):
    template_name = 'agents/agent_delete.html'
    def get_queryset(self):
        logged_in_management = self.request.user.userprofile
        return Agent.objects.filter(managed_by = logged_in_management)

    def get_success_url(self):
        return reverse('agent_list')

class AssignAgentView(ManagementAndLoginRequiredMixin, FormView):
    template_name = 'agents/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request' : self.request
        }) 

        return kwargs

    def get_success_url(self):
        return reverse('lead_list')

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent =agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

    
