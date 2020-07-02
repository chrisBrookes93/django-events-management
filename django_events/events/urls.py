from django.urls import path
from .views import view_event_list, EventCreate, view_event_attend, view_event_unattend, EventUpdate, EventView

urlpatterns = [
    path('', view_event_list, name='events_list'),
    path('<int:event_id>', EventView.as_view(), name='events_view'),
    path('edit/<int:pk>', EventUpdate.as_view(), name='events_edit'),
    path('create', EventCreate.as_view(), name='events_create'),
    path('attend_event/<int:event_id>', view_event_attend, name='events_attend'),
    path('unattend_event/<int:event_id>', view_event_unattend, name='events_unattend'),
]
