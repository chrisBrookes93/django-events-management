import os
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView

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
        return '/events/' + str(self.object.pk)

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
        return '/events/' + os.path.split(self.request.path)[-1]

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
        except Exception as e:
            logger.error(e)
            has_permission = False

        if not has_permission:
            logger.error('User %s attempted to modify an event that does not belong to them' % self.request.user)
        return has_permission

    def handle_no_permission(self):
        """
        Redirect to viewing the event when the user does not have permission to edit it
        """
        event_id = self.kwargs.get('pk', 0)
        return redirect('events_view', event_id=event_id)


@login_required()
def view_event_attend(request, event_id):
    """
    View to attend an event

    :param request: Request
    :param event_id: ID of the event (PK)
    """
    try:
        event = Event.objects.get_event(event_id)
        event.attendees.add(request.user)
        event.save()
        return redirect('events_view', event_id=event_id)
    except Exception as e:
        logger.error(e)
        return redirect('events_list')


@login_required()
def view_event_unattend(request, event_id):
    """
    View to unattend an event

    :param request: Request
    :param event_id: ID of the event (PK)
    """
    try:
        event = Event.objects.get_event(event_id)
        event.attendees.remove(request.user)
        event.save()
        return redirect('events_view', event_id=event_id)

    except Exception as e:
        logger.error(e)
        return redirect('events_list')


@login_required()
def view_event_view(request, event_id):
    """
    View to preview an event

    :param request: Request
    :param event_id: ID of the event (PK)
    """
    try:
        event = Event.objects.get_event(event_id)
        is_organiser = event.organiser == request.user
        user_is_attending = event.attendees.filter(pk=request.user.id).count() > 0
        return render(request,
                      'events/view_event.html',
                      {
                          'event': event,
                          'user_is_organiser': is_organiser,
                          'user_is_attending': user_is_attending
                      })
    except Exception as e:
        logger.error(e)
        return redirect('events_list')


@login_required
def view_event_list(request):
    """
    View to list events

    :param request: Request
    """
    query_filter = request.GET.get('filter', '')
    if query_filter == 'o':
        query_set = Event.objects.get_events_organised_by_user(request.user)
    elif query_filter == 'a':
        query_set = Event.objects.get_events_attended_by_user(request.user)
    elif query_filter == 'p':
        query_set = Event.objects.get_events_in_past()
    else:
        query_set = Event.objects.get_current_events()

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
