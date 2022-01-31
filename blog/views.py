from django.shortcuts import render, get_object_or_404

from .forms import CommentForm
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag


def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 4)

    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts.paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'posts': posts,
                                                   'page': page,
                                                   'tag': tag})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        #  коммент был отправлен
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #  если все ок, запиши данные в форму, но пока не сохраняй в базу
            new_comment = comment_form.save(commit=False)
            #  связь поста и коммента
            new_comment.post = post
            #  сохрани в бд
            new_comment.save()
    else:
        # в любом случае верни форму комментария
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form})

