from django.shortcuts import render, redirect
from django.views import View


class IndexView(View):

    def dispatch(self, request, *args, **kwargs):
        """
        View to display a welcome message, or redirect to the event list page if the user is authenticated

        :param request: Request
        """
        if request.user.is_authenticated:
            return redirect('events_list')
        else:
            return render(request, 'welcome.html')
