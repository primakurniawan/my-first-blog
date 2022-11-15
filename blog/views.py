from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category
from django.utils import timezone
from .forms import PostForm, CommentForm, GetForm
from django.db.models import Count
from django.http import QueryDict


# Create your views here.


def post_list(request):
    form = GetForm()
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date')
    categories = Category.objects.all()
    title = request.GET.get('title', False)
    if 'categories' in QueryDict(request.GET.urlencode(), mutable=True):
        categoriesSelected = QueryDict(
            request.GET.urlencode(), mutable=True).pop('categories')
        categoriesSelected = [eval(i) for i in categoriesSelected]
    else:
        categoriesSelected = []
    print(categoriesSelected)
    if title != '' and title:
        posts = posts.filter(title__contains=title)
        categories = Category.objects.filter(post__title__contains=title)

    if categoriesSelected != [] and categoriesSelected:
        posts = posts.filter(categories__pk__in=categoriesSelected).distinct()
        categories = Category.objects.filter(
            post__categories__pk__in=categoriesSelected).distinct()

    categories = categories.annotate(
        num_article=Count('post', distinct=True)).distinct()
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

            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(instance=post)
        comments = Comment.objects.all().filter(post__pk=pk)
        categories = Category.objects.filter(post__id=pk)

        return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form, 'categories': categories})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if 'categories' in QueryDict(request.POST.urlencode(), mutable=True):
            categoriesSelected = QueryDict(
                request.POST.urlencode(), mutable=True).pop('categories')
            categoriesSelected = [eval(i) for i in categoriesSelected]
        else:
            categoriesSelected = []

        if categoriesSelected != [] and categoriesSelected:
            categories = Category.objects.filter(
                post__categories__pk__in=categoriesSelected)
            print(categories)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            post.categories.add(*categoriesSelected)
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if 'categories' in QueryDict(request.POST.urlencode(), mutable=True):
            categoriesSelected = QueryDict(
                request.POST.urlencode(), mutable=True).pop('categories')
            categoriesSelected = [eval(i) for i in categoriesSelected]
        else:
            categoriesSelected = []

        if categoriesSelected != [] and categoriesSelected:
            categories = Category.objects.filter(
                post__categories__pk__in=categoriesSelected)
            print(categories)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            post.categories.add(*categoriesSelected)
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
