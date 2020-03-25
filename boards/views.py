from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.shortcuts import render_to_response
from .forms import NewTopicForm, PostForm
from .models import Board, Post, Topic, MFile
from django.contrib.gis.geos import Point

from accounts.forms import UserProfileForm, ProfileForm
from accounts.models import Profile, Survey
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory, formset_factory
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.core.serializers.json import DjangoJSONEncoder
import json
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

@login_required
def review(request):
    if request.method == 'POST':

        feeling = request.POST.get('feeling')
        category = request.POST['feedback_regarding']
        subcategory = request.POST['feedback_categories']
        bus_no = request.POST['bus_no']
        incident_date = request.POST['incident_date']
        incident_time = request.POST['incident_time']
        quick_review = request.POST['selectone']
        route_no  = request.POST['route_no']
        route_name = request.POST['route_name']
        bus_operator = request.POST['bus_operator']
        address = request.POST['locname']

        subject=request.POST['event']
        message=request.POST['comment']
        audit=request.POST.get('audit', None)
        lat = request.POST['lat']
        lon = request.POST['lon']
        pnt = Point(float(lon), float(lat))

        topic = Topic.objects.create(
            starter=request.user,
            board=Board.objects.get(id=category),
            feeling=feeling,
            category=category,
            subcategory=subcategory,
            bus_no=bus_no,
            incident_date=incident_date,
            incident_time=incident_time,
            quick_review=quick_review,
            route_no=route_no,
            route_name=route_name,
            bus_operator=bus_operator,
            message=message,
            address=address,
            audit=audit,
            subject=subject,
            location = pnt,
            views=1,
        )
        topic.save()
        for afile in request.FILES.getlist('upload_files'):
            MFile.objects.create(
                starter=request.user,
                board=Board.objects.get(id=category),
                topic=topic,
                afile=afile)
        MFile.objects.create(
            starter=request.user,
            board=Board.objects.get(id=category),
            topic=topic,
            afile='/nomap.jpg')


        Post.objects.create(
            message=message,
            topic=topic,
            created_by=request.user,
        )
        success = 10
        user = request.user
        user_form = UserProfileForm(instance=user)

        ProfileInlineFormset = inlineformset_factory(User, Profile, form=ProfileForm, can_delete=False)
        formset = ProfileInlineFormset(instance=user)

        data = Topic.objects.filter(starter=request.user).order_by('-id')[:8]
        files = MFile.objects.all()

        return render(request, "account_update.html", {
                        "user_form": user_form,
                        "profile_form": formset,
                        "success": success,
                        "data":data,
                        "files":files,
                    })

    return render(request, 'review.html')

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
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user,
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

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

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

def mapview(request):
    topicdatas = Topic.objects.all()

    return render(request, 'mapview.html', {'topicdatas' : topicdatas,})

def topicdata(request):

    topic_id = request.GET.get('myvar', None)
    data = {
        'am': topic_id,
        'i': 1,
    }

    return JsonResponse(data)

def popular(request):
    if request.method == 'POST':
        print('yes')

    return render(request, 'popular.html')