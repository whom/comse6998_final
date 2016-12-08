from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic

import json

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

class NewPostView(generic.ListView):
    template_name = 'webapp/post.html'

    def get_queryset(self):
        return True

def storePost(request):
    print "YEP"

    test = {}
    test['return'] = request.GET['title']
    
    return HttpResponse(json.dumps(test))