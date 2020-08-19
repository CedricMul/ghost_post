from django.shortcuts import render, reverse, HttpResponseRedirect

from ghost_app.models import GhostPost
from ghost_app.forms import PostForm

def index(request):
    posts = GhostPost.objects.order_by('-datetime')
    return render(request, 'index.html', {'posts': posts})

def post_form_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            GhostPost.objects.create(
                is_boast=data.get('is_boast'),
                content=data.get('content')
            )
            return HttpResponseRedirect(reverse('home'))

    form = PostForm()
    return render(request, 'post_form.html', {'form': form})

def upvote_view(request, id):
    post = GhostPost.objects.get(id=id)
    post.upvotes += 1
    post.total_votes += 1
    post.save()
    return HttpResponseRedirect(reverse('home'))

def downvote_view(request, id):
    post = GhostPost.objects.get(id=id)
    post.downvotes += 1
    post.total_votes -= 1
    post.save()
    return HttpResponseRedirect(reverse('home'))

def boast_view(request):
    posts = GhostPost.objects.filter(is_boast=True).order_by('-datetime')
    return render(request, 'index.html', {'posts': posts})

def roast_view(request):
    posts = GhostPost.objects.filter(is_boast=False).order_by('-datetime')
    return render(request, 'index.html', {'posts': posts})

def score_sort_view(request):
    posts = GhostPost.objects.order_by('-total_votes')
    return render(request, 'index.html', {'posts': posts})
