from django.contrib import admin
from .models import Lead, Agent, User, UserProfile, Category
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Lead)
admin.site.register(Agent)

