from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

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

'''
Currently just stubs. We'd need to call the helper Python functions in
post_functions.py to store them into the queue.
'''
def storePost(request):
    print "YEP"

    test = {}
    test['return'] = request.GET['title']
    
    return HttpResponse(json.dumps(test))

def storeComment(request):
    print "YEP"

    test = {}
    test['return'] = "Success! This is what was sent: " + request.GET['comment']

    return HttpResponse(json.dumps(test))

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        user_id = request.POST['userID']
        user_name = request.POST['userName']
    return HttpResponse