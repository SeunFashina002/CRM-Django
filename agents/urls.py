from django.urls import path
from .views import AgentCreateView, AgentListView, AgentUpdateView, AgentDeleteView, AgentDetailView

urlpatterns = [
    path('agents/', AgentListView.as_view(), name='agent_list'),
    path('create-agent/', AgentCreateView.as_view(), name='agent_create'),
    path('agents/<int:pk>/update-agent/', AgentUpdateView.as_view(), name='agent_update'),
    path('agents/<int:pk>/delete-agent/', AgentDeleteView.as_view(), name='agent_delete'),
    path('agents/<int:pk>/', AgentDetailView.as_view(), name='agent_detail'),
]

