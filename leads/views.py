from django.shortcuts import render, redirect
from .models import Lead
from .forms import LeadForm

# this view render the homepage
def index(request):
    return render(request, 'index.html')

# this view query all the leads in the database
def lead_list(request):

    leads = Lead.objects.all()
    context = {
        'leads' : leads
    }
    return render(request, 'lead_list.html', context)


#the value for this pk is coming from our lead_list.html in lead.id
#it is then passed to the concerned url in urls.py and the page
# the view attached to the url recieves the value of lead.id and render template base on the query in the view

def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead' : lead
    }
    return render(request, 'lead_detail.html', context)
    

# this view render the form that creates new leads
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

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('lead_list')