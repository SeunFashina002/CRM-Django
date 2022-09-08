from django import forms
from .models import Lead, User
from django.contrib.auth.forms import UserCreationForm, UsernameField

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'description',
            'phone_number',
            'email',
            'agent',
        )

#we are creating our custom form because in our model we inherited from abstract user. There will be a conflict

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        field_classes = {'username': UsernameField}

class LeadCategoryUpdateForm(forms.ModelForm):
        class Meta:
            model = Lead
            fields = (
                'category',
            )

    