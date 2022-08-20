from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, CreateView
from django.contrib.auth.forms import UserCreationForm
from .models import Lead
from .forms import LeadForm, CustomUserForm

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


class LeadDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'lead_delete.html'
    queryset = Lead.objects.all()
    
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

    
    