from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from events.models import Event, EventQuerySet
from events.serializers import EventListSerializer, EventDetailSerializer
from .permissions import IsEventOrganiser


@api_view(['GET'])
def api_root(request, format=None):
    """
    Renders the root of the API, displaying a top level view of the API endpoints
    """
    return Response({
        'events': reverse('event-list', request=request, format=format)
    })


class EventViewSet(ModelViewSet):
    serializer_class = EventListSerializer
    permission_classes = [IsAuthenticated, IsEventOrganiser]

    """
    Lookup dictionary for string-based filter
    """
    filter_func_lookup = {
        'o': Event.objects.get_events_organised_by_user,
        'a': Event.objects.get_events_attended_by_user,
        'p': Event.objects.get_events_in_past
    }

    def get_queryset(self):
        """
        Return the queryset, calling a specific function depending of the filter the user has provided
        """
        # Check if a filter has been specified
        query_filter = self.request.query_params.get('filter', '')
        # Get the function we need to call
        filter_func = self.filter_func_lookup.get(query_filter, Event.objects.get_current_events)
        # Obtain the query set
        query_set = filter_func(self.request.user)
        return query_set

    def retrieve(self, request, *args, **kwargs):
        """
        Override the retrieve() so that the EventQuerySet.get_event() is used as this adds annotations that we return
        in the response. We also return EventDetailSerializer which provides more information (namely the names/emails
        of the attendees)
        """
        event = Event.objects.get_event(user=self.request.user, **self.kwargs)
        if not event:
            return Response(status=HTTP_404_NOT_FOUND)
        serializer = EventDetailSerializer(event)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Custom override to patch in the organiser as the current user
        """
        serializer.save(organiser=self.request.user)

    @action(detail=True, methods=['POST'])
    def attend(self, request, pk, *args, **kwargs):
        """
        API endpoint to mark the current user as attending a given event
        """
        event = Event.objects.get_event(pk=pk, user=self.request.user)
        if not event:
            return Response(status=HTTP_404_NOT_FOUND)
        if event.is_in_past:
            return Response(status=HTTP_403_FORBIDDEN, data={'detail': 'Cannot attend an event in the past'})

        event.attendees.add(request.user)
        return Response(status=HTTP_202_ACCEPTED, data={'detail': 'Successfully attended'})

    @action(detail=True, methods=['POST'])
    def unattend(self, request, *args, **kwargs):
        """
        API endpoint to remove the current user as an attendee of a given event
        """
        event = Event.objects.get_event(user=self.request.user, **self.kwargs)
        if not event:
            return Response(status=HTTP_404_NOT_FOUND)
        if event.is_in_past:
            return Response(status=HTTP_403_FORBIDDEN, data={'detail': 'Cannot unattend an event in the past'})

        event.attendees.remove(request.user)
        return Response(status=HTTP_202_ACCEPTED, data={'detail': 'Successfully unattended'})
