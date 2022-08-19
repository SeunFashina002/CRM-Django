from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#users are basically agents
class User(AbstractUser):
    pass

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
    # in other word agent is our logged in user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
