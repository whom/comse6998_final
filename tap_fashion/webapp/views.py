from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic


class IndexView(generic.ListView):
    """
    Creates the view for the home page of the app
    """
    template_name = 'webapp/index.html'

    def get_queryset(self):
        return True



class DashboardView(generic.ListView):
    """
    Creates the view for the dashboard page of the app
    """
    template_name = 'webapp/dashboard.html'

    def get_queryset(self):
        return True
