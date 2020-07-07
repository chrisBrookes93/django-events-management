import logging
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, TemplateView, UpdateView, CreateView
from django.http import HttpResponseForbidden

from .models import Event
from .forms import EventForm

logger = logging.getLogger(__name__)


class EventCreate(LoginRequiredMixin, CreateView):
    """
    View to create an event
    """

    model = Event
    fields = ['title', 'date_time', 'description']
    template_name = 'events/create_event.html'

    def form_valid(self, form):
        """
        Patch in the organiser to resolve the foreign key

        :param form: form submitted
        """
        form.instance.organiser = self.request.user
        return super(EventCreate, self).form_valid(form)


class EventUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to edit an event
    """
    template_name = 'events/edit_event.html'
    form_class = EventForm
    model = Event

    def test_func(self):
        """
        Permissions check to make sure that the current user is the event organiser

        :return: True if the user is the organiser, else False
        :rtype: bool
        """
        event = self.get_object()
        return self.request.user == event.organiser

    def handle_no_permission(self):
        """
        Return a forbidden HTTP error if the current user fails the permissions check
        """
        return HttpResponseForbidden()


class EventView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        """
        Render the basic web page that displays a given event. The actual data is retrieved from the API via AJAX, so
        only the pk is passed into the template
        """
        return render(request,
                      'events/view_event.html',
                      {'pk': pk})


FILTER_FUNC_TABLE = {
    'o': Event.objects.get_events_organised_by_user,
    'a': Event.objects.get_events_attended_by_user,
    'p': Event.objects.get_events_in_past
}


class EventList(LoginRequiredMixin, TemplateView):

    def get(self, request,  *args, **kwargs):
        """
        Renders a template to display the list of events
        """
        # Check if the GET request has an event filter in it
        query_filter = request.GET.get('filter')
        # Use the specific QuerySet function based on the event filter
        filter_func = FILTER_FUNC_TABLE.get(query_filter, Event.objects.get_current_events)
        query_set = filter_func(request.user)

        page = request.GET.get('page', 1)
        paginator = Paginator(query_set, 10)
        try:
            event_list = paginator.page(page)
        except PageNotAnInteger:
            event_list = paginator.page(1)
        except EmptyPage:
            event_list = paginator.page(paginator.num_pages)

        return render(request,
                      'events/list_events.html',
                      {
                          'events': event_list,
                          'query_filter': query_filter
                      })
