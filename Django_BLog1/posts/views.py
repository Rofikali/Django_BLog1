from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages













from .forms import PostCreateForm
from django.urls import reverse
from .models import Posts


from django.core.paginator import Paginator

from django.db.models import Q


def home(request):
    # all_data = Posts.objects.all().order_by('-timestamp')
    query_list = Posts.objects.all()
    query = request.GET.get('q')
    if query:
        query_list = query_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

    paginator = Paginator(query_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print()
    print('Searching here --->', page_obj)
    context = {
        # 'all_data': all_data,
        'page_obj': page_obj,
        'title': 'Home Page'
    }
    return render(request, 'posts/posts.html', context)

    # context = {
    #     'all_data': Posts.objects.all().order_by('-timestamp'),
    #     'title': 'Home Page'
    # }
    # return render(request, 'posts/posts.html', context)


def post_detail(request, id=None):
    data = get_object_or_404(Posts, id=id)

    context = {
        'title': 'Detail Post',
        'data': data
    }
    return render(request, 'posts/post.html', context)


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponseRedirect(reverse('posts:home'))
    # else:

    form = PostCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        # print(form.cleaned_data.get('title'))
        instance.save()
        # redirect to a new URL:
        messages.add_message(request, messages.SUCCESS,
                             'Successfully created !', extra_tags='so more')
        return HttpResponseRedirect(reverse('posts:post-detail', args=(instance.id,)))

    context = {
        'title': 'Creating Post',
        'form': form
    }
    return render(request, 'posts/create.html', context)

    # One way is this
    '''
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostCreateForm(request.POST)
        
            we can see like these
            print(request.POST.get('title'))
            print(request.POST.get('content'))
       
        title = request.POST.get('title')
        cre = Posts.objects.create(title=title)
        cre.save()
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save()
            # redirect to a new URL:
            return redirect('/')
    context = {
        'title': 'Creating Post',
        'form': PostCreateForm
    }
    return render(request, 'posts/create.html', context)
    '''


def post_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponseRedirect(reverse('posts:home'))

    instance = get_object_or_404(Posts, pk=id)
    if not instance.user == request.user:
        return HttpResponseRedirect(reverse('posts:home'))
        # return HttpResponse({'Both are same here'})
    else:
        form = PostCreateForm(request.POST or None, request.FILES or None,
                              instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.user = request.user # this is not working here
            instance.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Successfully Updated !')
            return HttpResponseRedirect(reverse('posts:post-detail', args=(instance.id,)))

    context = {
        'form': form,
        'title': 'Update Post',
    }
    return render(request, 'posts/update.html', context)


'''
    # this is one way '''
'''
    data = get_object_or_404(Posts, pk=id)
    form = PostCreateForm(instance=data)
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            # Do something.
            # redirect to a new URL:
            messages.add_message(request, messages.SUCCESS,
                                 'Successfully Updated !')
            return HttpResponseRedirect(reverse('posts:post-detail', args=(instance.id,)))
        else:
            form = PostCreateForm(initial=data)
            return HttpResponseRedirect(reverse('posts:post-detail', args=(instance.id,)))

    context = {
        'form': form,
        'title': 'Update Post'
    }
    '''

# return render(request, 'posts/update.html', {'form': form})
# return render(request, 'posts/update.html', context)


def post_delete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponseRedirect(reverse('posts:home'))

    instance = get_object_or_404(Posts, id=id)
    # instance.user = request.user # not working here
    if not instance.user == request.user:
        return HttpResponseRedirect(reverse('posts:home'))
    instance.delete()
    return redirect('posts:home')
