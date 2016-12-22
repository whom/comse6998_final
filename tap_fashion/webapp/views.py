from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import post_functions
import comment_functions
from get_functions import *
import random

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
    #template_name = 'webapp/dashboard.html'

    def get(self,request):

        all_posts_list = getAllPosts()
        random.shuffle(all_posts_list)
        posts_list = all_posts_list[:10]

        for post in posts_list:
            post['post_id'] = str(post['post_id'])
            post['comments'].append("this is a new comment")
            post['comments'].append("yay! this is just a comment")
            post['comments'].append(post['post_id']);
        return render(request, 'webapp/dashboard.html',
                      {'esPosts': posts_list})

class NewPostView(generic.ListView):
    template_name = 'webapp/post.html'

    def get_queryset(self):
        return True

class RelatedPostsView(generic.ListView):
    template_name = 'webapp/related.html'

    def get_queryset(self):
        return True

    def get(self, request):
        posts_list = []
        post_id = request.GET.get('postId')

        related_posts = post_functions.findRelatedPosts(post_id)

        if related_posts:
            for post in related_posts['related_posts']:
                posts_list.append(buildWholePost(post['post_id']))

            return render(request, 'webapp/related.html',
                         {'relatedPosts': posts_list})
        else:
            print "Nope."
            return HttpResponse()

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
    text = request.GET['comment']

    newComment = comment_functions.createComment(post_id, user_id, user_name, text)
    comment_functions.storeComment(newComment)

    return HttpResponse("success")

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        user_id = request.POST['userID']
        user_name = request.POST['userName']
    return HttpResponse