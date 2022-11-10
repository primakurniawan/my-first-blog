from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category
from django.utils import timezone
from .forms import PostForm, CommentForm, GetForm
from django.db.models import Count


# Create your views here.


def post_list(request):
    form = GetForm()
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date')
    categories = Category.objects.all()
    title = request.GET.get('title', False)
    category = request.GET.get('category', False)
    if title != '' and title:
        posts = posts.filter(title__contains=title)
        categories = Category.objects.filter(post__title__contains=title)

    if category != '' and category:
        posts = posts.filter(category__pk=category)
        categories = Category.objects.filter(post__category__pk=category)

    categories = categories.annotate(num_article=Count('post'))
    return render(request, 'blog/post_list.html', {'posts': posts, 'form': form, 'categories': categories})


def post_detail(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, pk=pk)
            comment = form.save(commit=False)
            comment.user = request.user
            comment.created_at = timezone.now()
            comment.post = post
            comment.user = request.user

            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(instance=post)
        comments = Comment.objects.all().filter(post__pk=pk)
        categories = Category.objects.filter(post__id=2)

        return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form, 'categories': categories})


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
