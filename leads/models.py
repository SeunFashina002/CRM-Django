from unicodedata import category
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_management = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


#leads are clients or customers
class Lead(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    managed_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('Category', related_name='leads', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

#agent are assigned to leads
#an agent can be assigned to more than one lead or client(foreignKey == 1 to many)

class Category(models.Model):
    name = models.CharField(max_length=30)
    managed_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Agent(models.Model):
    
    #we are creating an agent with a registered user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # we are managing agents under the managed by 
    managed_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance) 
        #This signal listen for user creation event 
        #once a user is created from our UI, it automatically create a userprofile for that user
        #instance is basically the name of the user so we are assigning the name of the user as a profile

post_save.connect(post_user_created_signal, sender=User)