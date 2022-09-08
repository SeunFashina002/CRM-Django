from unicodedata import category
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, CreateView, DetailView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Lead
from .forms import LeadForm, CustomUserForm, LeadCategoryUpdateForm
from agents.mixins import ManagementAndLoginRequiredMixin

# this view render the homepage
def index(request):
    return render(request, 'index.html')

# this view query all the leads in the database
@login_required(login_url='/login')
def lead_list(request):

    leads = Lead.objects.all()
    context = {
        'leads' : leads
    }
    return render(request, 'lead_list.html', context)



class LeadListView(LoginRequiredMixin, ListView):
    template_name = 'lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        logged_in_user = self.request.user

        if logged_in_user.is_management:
            queryset = Lead.objects.filter(managed_by = logged_in_user.userprofile,  agent__isnull=False)
        else:

            # if the logged in user is an agent filter leads by the user managing the agent
            queryset = Lead.objects.filter(managed_by = logged_in_user.agent.managed_by,  agent__isnull=False)

            # if the logged in user is an agent filter leads by the agent who is currently logged
            queryset = queryset.filter(agent__user=logged_in_user)

        return queryset

    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        logged_in_user = self.request.user
        if logged_in_user.is_management:
            #filter by logged_in_management and foreign key agent that has null value
            queryset = Lead.objects.filter(managed_by = logged_in_user.userprofile,  agent__isnull=True)
            context.update({
                'unassigned_leads':queryset,
            })
        return context


#the value for this pk is coming from our lead_list.html in lead.id
#it is then passed to the concerned url in urls.py and the page
# the view attached to the url recieves the value of lead.id and render template base on the query in the view

@login_required(login_url='/login')
def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead' : lead
    }
    return render(request, 'lead_detail.html', context)
    
class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        logged_in_user = self.request.user

        if logged_in_user.is_management:
            queryset = Lead.objects.filter(managed_by = logged_in_user.userprofile)
        else:
            queryset = Lead.objects.filter(managed_by = logged_in_user.agent.managed_by)

            # if the logged in user is an agent filter by the agent whose user is our logged in user
            queryset = queryset.filter(agent__user=logged_in_user)

        return queryset


# this view render the form that creates new leads
@login_required(login_url='/login')
def lead_create(request):
    form = LeadForm()
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
        else:
            form = LeadForm()
            print('We could not process your request')
    context= {
        'form' : form,
    }
    return render(request, 'lead_create.html', context)


class LeadCreateView(ManagementAndLoginRequiredMixin, CreateView):
    template_name = 'lead_create.html'
    form_class = LeadForm

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.managed_by = self.request.user.userprofile
        lead.save()
        return super(LeadCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('lead_list')




@login_required(login_url='/login')
def lead_update(request, pk):
    # get the specific lead you want to update
    lead = Lead.objects.get(id=pk)
    # pass that specific lead as instance to the form to be rendered
    form = LeadForm(instance=lead)
    if request.method == 'POST':
        # pass that specific lead as instance to the form to be rendered and fill it with the data the user entered 
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
        else:
            form = LeadForm()
    context = {
        'form' : form,
        'lead' : lead
    }
    return render(request, 'lead_update.html', context)


class LeadUpdateView(ManagementAndLoginRequiredMixin, UpdateView):
    form_class = LeadForm
    template_name = 'lead_update.html'

    def get_queryset(self):
        logged_in_user = self.request.user
        return Lead.objects.filter(managed_by=logged_in_user.userprofile)

    def get_success_url(self):
        return reverse('lead_list')



class LeadDeleteView(ManagementAndLoginRequiredMixin, DeleteView):
    template_name = 'lead_delete.html'
    def get_queryset(self):
        logged_in_user = self.request.user
        return Lead.objects.filter(managed_by=logged_in_user.userprofile)

    
    def get_success_url(self):
        return reverse('lead_list')


class Login(LoginView):
    template_name = 'registration/login.html'


# CustomuserForm is defined in my forms.py
class Signup(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserForm

    def get_success_url(self):
        return reverse('login')

    
class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        logged_in_user = self.request.user

        #filter out the leads that doesn't fall in any category(i.e new or unassigned lead)
        if logged_in_user.is_management:
            queryset = Lead.objects.filter(managed_by = logged_in_user.userprofile, category__isnull=True)
        else:
            queryset = Lead.objects.filter(managed_by = logged_in_user.agent.managed_by,  category__isnull=True)
               
        context.update({
            'unassigned_leads_count':queryset.filter().count(),
        })
        return context


    def get_queryset(self):
        logged_in_user = self.request.user

        if logged_in_user.is_management:
            #filter our category for the currently logged in management excluding other management data
            queryset = Category.objects.filter(managed_by = logged_in_user.userprofile)
        else:

            # if the logged in user is an agent filter category for the agent associated to a particular management
            #in other words an agent can't the details of other management or agent
            queryset = Category.objects.filter(managed_by = logged_in_user.agent.managed_by)

        return queryset

class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)

        #self.get_object gets the category object 
        # .leads.all() gets all leads that falls under this category object e.g(contacted)
        leads = self.get_object().leads.all()

        context.update({
            'leads':leads,
        })
        return context



    def get_queryset(self):
        logged_in_user = self.request.user

        if logged_in_user.is_management:
            queryset = Category.objects.filter(managed_by = logged_in_user.userprofile)
        else:
            queryset = Category.objects.filter(managed_by = logged_in_user.agent.managed_by)

        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    form_class = LeadCategoryUpdateForm
    template_name = 'lead_category_update.html'

    def get_queryset(self):
        logged_in_user = self.request.user
        if logged_in_user.is_management:
            queryset = Lead.objects.filter(managed_by = logged_in_user.userprofile)
        else:
            queryset = Lead.objects.filter(managed_by = logged_in_user.agent.managed_by)
        return queryset

    def get_success_url(self):
        return reverse('lead_detail', kwargs={'pk':self.get_object().id})

