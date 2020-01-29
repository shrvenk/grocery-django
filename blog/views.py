from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm,RegForm,LoginForm
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth import login as auth_login,logout
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from .utility import *
from django.urls import reverse 
#from rest_framework.views import APIView
#from rest_framework.response import Response
#from rest_framework import status
#from .serializers import PostSerializer

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

#class Post_API_list(APIView):
    #def get(self,request):
        #API_posts = Post.objects.all()
        #serializer = PostSerializer(API_posts , many=True)
        #return Response(serializer.data)

    #def post(self):
        #pass

class RegFormview(View):

    def post(self,request):
        form = RegForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request=request, user=user)
                return HttpResponseRedirect(reverse('post_list'))
        msg_to_html = custom_message('Invalid Credentials', TagType.danger)
        dictionary = dict(request=request, messages = msg_to_html)
        dictionary.update(csrf(request))
        return render(request,'blog/post_list.html', dictionary)

  
def LoginFormview(request):
     if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request=request, user=user)
            return HttpResponseRedirect(reverse('post_list'))
        else:
            msg_to_html = custom_message('Invalid Credentials', TagType.danger)
            dictionary = dict(request=request, messages = msg_to_html)
            dictionary.update(csrf(request))
        return render(request,'blog/post_list.html', dictionary)
    
def Logout_view(request):
    logout(request)
    return redirect('post_list')

def main_base(request):
    dictionary = dict(request=request)
    dictionary.update(csrf(request))
    return render(request,'blog/base.html', dictionary)

    


