from django.shortcuts import render, redirect


def view_index(request):
    """
    View to display a welcome message, or redirect to the event list page if the user is authenticated

    :param request: Request
    """
    if request.user.is_authenticated:
        return redirect('events_list')
    else:
        return render(request, 'welcome.html')
