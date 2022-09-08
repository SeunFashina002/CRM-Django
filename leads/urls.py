from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from .views import index, LeadListView, LeadUpdateView, LeadCreateView, LeadDetailView, LeadDeleteView, Login, Signup, CategoryListView, CategoryDetailView, LeadCategoryUpdateView
from agents.views import AssignAgentView
urlpatterns = [
    path('', index, name='home'),
    path('login/', Login.as_view() , name='login'),
    path('reset-password/', PasswordResetView.as_view() , name='reset-password'),
    path('password-reset-done/', PasswordResetDoneView.as_view() , name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view() , name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view() , name='password_reset_complete'),
    path('signup/', Signup.as_view() , name='signup'),
    path('logout/', LogoutView.as_view() , name='logout'),
    path('leads/', LeadListView.as_view(), name='lead_list'),
    path('category/', CategoryListView.as_view(), name='category_list'),

    path('leads/<int:pk>/', LeadDetailView.as_view() , name='lead_detail'),
    path('category/<int:pk>/', CategoryDetailView.as_view() , name='category_detail'),

    path('leads/<int:pk>/update/', LeadUpdateView.as_view() , name='lead_update'),
    path('category/<int:pk>/update/', LeadCategoryUpdateView.as_view() , name='lead_category_update'),

    path('leads/<int:pk>/delete/', LeadDeleteView.as_view() , name='lead_delete'),
    path('leads/<int:pk>/assign-agent/', AssignAgentView.as_view() , name='assign_agent'),

    path('create/', LeadCreateView.as_view(), name='lead_create'),
]

