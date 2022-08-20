from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.

#users are basically agents
class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


#leads are clients or customers
class Lead(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

#agent are assigned to leads
#an agent can be assigned to more than one lead or client(foreignKey == 1 to many)


class Agent(models.Model):
    #since user is agent, assign them to eachother 1user == 1 agent(OneToOneField)
    # in other word agent is our logged in user because we are creating an agent with a registered user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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