from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import index, lead_list, lead_detail, lead_create, lead_update, LeadDeleteView, Login, Signup

urlpatterns = [
    path('', index, name='home'),
    path('login/', Login.as_view() , name='login'),
    path('signup/', Signup.as_view() , name='signup'),
    path('logout/', LogoutView.as_view() , name='logout'),
    path('leads/', lead_list, name='lead_list'),
    path('leads/<int:pk>/', lead_detail , name='lead_detail'),
    path('leads/<int:pk>/update/', lead_update , name='lead_update'),
    path('leads/<int:pk>/delete/', LeadDeleteView.as_view() , name='lead_delete'),
    path('create/', lead_create, name='lead_create'),

]

