from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .forms import NewTopicForm, PostForm
from .models import Board, Topic, Post, News
from django.contrib.auth.decorators import login_required


# Create your views here.
def activity_news_content(request, pk):
    activity_news_contents = get_object_or_404(News, pk=pk)
    activity_news_contents.views += 1
    activity_news_contents.save()
    return render(request, 'activity_news_content.html', {'activity_news_contents': activity_news_contents})


def activity_news(request):
    activity_news_list = News.objects.filter(type='A').order_by('-created_at')
    return render(request, 'activity_news.html', {'activity_news_list': activity_news_list})


def noting_news_content(request, pk):
    noting_news_contents = get_object_or_404(News, pk=pk)
    noting_news_contents.views += 1
    noting_news_contents.save()
    return render(request, 'noting_news_content.html', {'noting_news_contents': noting_news_contents})


def noting_news(request):
    noting_news_list = News.objects.filter(type='N').order_by('-created_at')
    return render(request, 'noting_news.html', {'noting_news_list': noting_news_list})


def study_news_content(request, pk):
    study_news_contents = get_object_or_404(News, pk=pk)
    study_news_contents.views += 1
    study_news_contents.save()
    return render(request, 'study_news_content.html', {'study_news_contents': study_news_contents})


def study_news(request):
    study_news_list = News.objects.filter(type='S').order_by('-created_at')
    return render(request, 'study_news.html', {'study_news_list': study_news_list})


def maps(request):
    return render(request, 'map.html')


def home(request):
    try:
        latest_six_study_news = News.objects.filter(type='S').order_by('-created_at')[:6]
        latest_six_notifying_news = News.objects.filter(type='N').order_by('-created_at')[:6]
        latest_six_activity_news = News.objects.filter(type='A').order_by('-created_at')[:6]
    except News.DoesNotExist:
        raise Http404("News does not exist!")
    return render(request, 'home.html', {'latest_six_study_news': latest_six_study_news,
                                         'latest_six_notifying_news': latest_six_notifying_news,
                                         'latest_six_activity_news': latest_six_activity_news})


def board(request):
    boards = Board.objects.all()
    return render(request, 'boards.html', {'boards': boards})


@login_required()
def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    # topics = board.topics.exclude(starter=request.user).order_by('-last_updated').annotate(replies=Count('posts'))
    return render(request, 'topics.html', {'board': board, 'topics': topics})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            # return redirect('board_topics', pk=board.pk)
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()

    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()

    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})
