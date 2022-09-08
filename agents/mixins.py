from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class ManagementAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is part of management."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_management:
            return redirect("lead_list")
        return super().dispatch(request, *args, **kwargs)