from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import post_functions
import comment_functions

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

class RelatedPostsView(generic.ListView):
    template_name = 'webapp/related.html'

    def get_queryset(self):
        return True

'''
Currently just stubs. We'd need to call the helper Python functions in
post_functions.py to store them into the queue.
'''
def storePost(request):
    print "Generating a new post!"
    title = request.GET['title']
    text = request.GET['text']
    user_name = request.GET['username']
    user_id = request.GET['userid']
    image_url = request.GET['image']

    newPost = post_functions.createPost(title, user_id, text, user_name, images=[image_url])
    post_functions.storePost(newPost)
    
    return HttpResponse("success")

def storeComment(request):
    user_id = request.GET['userid']
    user_name = request.GET['username']
    post_id = request.GET['post_id']
    text = request.GET['text']

    newComment = comment_functions.createComment(post_id, user_id, user_name, text)
    comment_functions.storeComment(newComment)

    return HttpResponse("success")

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        user_id = request.POST['userID']
        user_name = request.POST['userName']
    return HttpResponse