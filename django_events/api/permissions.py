from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEventOrganiser(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Custom permission check to only allow the event organiser to make changes to an event
        """
        # Any user is allowed to view the event, so allow all safe methods
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the organiser of the event.
        return obj.organiser == request.user
