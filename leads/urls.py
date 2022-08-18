from django.urls import path

from .views import index, lead_list, lead_detail, lead_create, lead_update, lead_delete

urlpatterns = [
    path('', index, name='home'),
    path('leads/', lead_list, name='lead_list'),
    path('leads/<int:pk>/', lead_detail , name='lead_detail'),
    path('leads/<int:pk>/update/', lead_update , name='lead_update'),
    path('leads/<int:pk>/delete/', lead_delete , name='lead_delete'),
    path('create/', lead_create, name='lead_create'),

]

