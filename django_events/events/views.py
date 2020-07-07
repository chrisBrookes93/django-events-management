import logging
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import View, TemplateView
from django.http.response import HttpResponseNotFound, HttpResponseForbidden

from .models import Event

logger = logging.getLogger(__name__)


class EventCreate(LoginRequiredMixin, CreateView):
    """
    View to create an event
    """

    model = Event
    fields = ['title', 'date_time', 'description']
    template_name = 'events/create_event.html'

    def get_success_url(self):
        """
        Build the URL to view the event just created

        :return: URL to view the event just created
        :rtype: str
        """
        return reverse('events_view', args=(self.object.id,))

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

    model = Event
    fields = ['title', 'date_time', 'description']
    template_name = 'events/edit_event.html'

    def get_success_url(self):
        """
        Build the URL to view the event just modified

        :return: URL to view the event just modified
        :rtype: str
        """
        return reverse('events_view', args=(self.object.id,))

    def test_func(self):
        """
        Permissions check to make sure that the current user is the event organiser

        :return: True if the user is the organiser, else False
        :rtype: bool
        """
        event_id = self.kwargs.get('pk', 0)
        try:
            event = Event.objects.get(pk=event_id)
            has_permission = self.request.user == event.organiser
        except Event.DoesNotExist:
            has_permission = False

        return has_permission

    def handle_no_permission(self):
        """
        Redirect to viewing the event when the user does not have permission to edit it
        """
        return HttpResponseForbidden()


class EventView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        try:
            event = Event.objects.get_event(pk, request.user)
            if not event:
                return HttpResponseNotFound()

            if event.is_attending:
                attendance_url = reverse('event-unattend', args=(event.id,))
            else:
                attendance_url = reverse('event-attend', args=(event.id,))

            return render(request,
                          'events/view_event.html',
                          {'event': event,
                           'attendance_url': attendance_url})
        except Exception as e:
            logger.error(e)
            return redirect('events_list')


FILTER_FUNC_TABLE = {
    'o': Event.objects.get_events_organised_by_user,
    'a': Event.objects.get_events_attended_by_user,
    'p': Event.objects.get_events_in_past
}


class EventList(LoginRequiredMixin, TemplateView):

    def get(self, request,  *args, **kwargs):
        query_filter = request.GET.get('filter')
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
