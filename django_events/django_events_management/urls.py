from django.contrib import admin
from django.urls import path, include
from .views import view_index

urlpatterns = [
    path('', view_index, name='index'),
    path('admin', admin.site.urls),
    path('events/', include('events.urls')),
    path('users/', include('users.urls')),
    path('api/', include('api.urls'))
]
