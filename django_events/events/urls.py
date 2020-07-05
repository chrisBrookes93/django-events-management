from django.urls import path
from .views import EventCreate, AttendEvent, UnattendEvent, EventUpdate, EventView, EventList

urlpatterns = [
    path('', EventList.as_view(), name='events_list'),
    path('<int:pk>', EventView.as_view(), name='events_view'),
    path('edit/<int:pk>', EventUpdate.as_view(), name='events_edit'),
    path('create', EventCreate.as_view(), name='events_create'),
    path('attend_event/<int:pk>', AttendEvent.as_view(), name='events_attend'),
    path('unattend_event/<int:pk>', UnattendEvent.as_view(), name='events_unattend'),
]
