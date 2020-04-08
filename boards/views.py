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
from .models import Board, Post, Topic, MFile, Comment, Vote
from django.contrib.gis.geos import Point

from accounts.forms import UserProfileForm, ProfileForm
from accounts.models import Profile, Survey
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory, formset_factory
from django.http import JsonResponse, HttpResponse
from notify.signals import notify
from django.template.loader import render_to_string
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

class CommentListView(ListView):
    model = Post
    context_object_name = 'comments'
    template_name = 'post_comments.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.post.pk)
        if not self.request.session.get(session_key, False):
            # self.topic.views += 1
            # self.topic.save()
            self.request.session[session_key] = True
        kwargs['post'] = self.post
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        queryset = self.post.comments.order_by('created_at')
        return queryset

def review(request):
    return render(request, 'review.html')

@login_required
def feedback(request):
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

        if not request.FILES.getlist('upload_files'):
            MFile.objects.create(
                starter=request.user,
                board=Board.objects.get(id=category),
                topic=topic,
                afile='/nomap.png')


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

        fn = request.user.username[0]

        notify.send(request.user, recipient_list=list(User.objects.exclude(id=request.user.id)), actor=request.user, actor_url = fn , verb="posted a new review.",
                    nf_type="followed_by_one_user")

        return render(request, "account_update.html", {
                        "user_form": user_form,
                        "profile_form": formset,
                        "success": success,
                        "data":data,
                        "files":files,
                    })

    if request.GET.get('lat'):
        return render(request, 'feedback_map.html', {'lat':request.GET.get('lat'), 'lon':request.GET.get('lon')})
    else:
        return render(request, 'feedback.html')

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
def reply_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.created_by = request.user
            comment.save()

            post.last_updated = timezone.now()
            post.save()

            print(post.get_page_count())

            post_url = reverse('post_comments', kwargs={'post_pk': post_pk})
            post_comment_url = '{url}?page={page}#{id}'.format(
                url=post_url,
                id=comment.pk,
                page=post.get_page_count()
            )

            return redirect(post_comment_url)
    else:

        form = PostForm()
    return render(request, 'reply_comment.html', {'post': post, 'form': form})


@method_decorator(login_required, name='dispatch')
class CommentUpdateView(UpdateView):
    model = Comment
    fields = ('message', )
    template_name = 'edit_comment.html'
    pk_url_kwarg = 'comment_pk'
    context_object_name = 'comment'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.updated_by = self.request.user
        comment.updated_at = timezone.now()
        comment.save()
        return redirect('post_comments', post_pk=comment.post.pk)


def mapview(request):

    topicdatas = Topic.objects.all()

    # post_list = Post.objects.all()
    # page=request.GET.get('page')
    # paginator = Paginator(post_list, 20)
    # try:
    #     posts = paginator.page(page)
    # except PageNotAnInteger:
    #     posts = paginator.page(1)
    # except EmptyPage:
    #     posts = paginator.page(paginator.num_pages)


    if request.method == 'POST':
        if request.user.is_authenticated:
            for afile in request.FILES.getlist('upload_files'):
                MFile.objects.create(
                    starter=request.user,
                    board=Board.objects.get(id=request.POST['ucat_id']),
                    topic=Topic.objects.get(id=request.POST['server_topic_id']),
                    afile=afile)
            Post.objects.create(
                message=request.POST['comment'],
                topic=Topic.objects.get(id=request.POST['server_topic_id']),
                created_by=request.user,
            )
        else:

            return redirect('login')
    # return render(request, 'mapview.html', {'topicdatas' :  topicdatas, 'page':page, 'posts':posts,})
    return render(request, 'mapview.html', {'topicdatas' :  topicdatas,})


def updatetopicdata(request):
    if request.user.is_authenticated:
        post_value = int(request.GET.get('vote', None))
        post_id = request.GET.get('postid', None)
        obj, created = Vote.objects.get_or_create(post=Post.objects.get(id=post_id), created_by=request.user)
        if post_value < 0:
            obj.down_vote += 1

        else:
            obj.up_vote += 1

        if abs(obj.up_vote - obj.down_vote) > 1:
            return JsonResponse({'status': 'fail', })
        else:
            obj.save()

        votes = Post.objects.get(id=post_id).vote + int(request.GET.get('vote', None))

        if votes < 0:
            return JsonResponse({'status': 'fail', })
        Post.objects.filter(id=post_id).update(vote=votes)


        return JsonResponse({'status':'success',})
    else:
        return JsonResponse({'status': 'login', })

def topicdata(request):

    topic_id = request.GET.get('myvar', None)
    mfiles = MFile.objects.filter(topic=topic_id)
    mfilelist = []
    # print(mfiles.count());
    for mfile in mfiles:
        if mfile.afile.url == "/media/nomap.png" and mfiles.count() > 1:
            continue;
        mfilelist.append(mfile.afile.url)

    topic = Topic.objects.get(id=topic_id)
    uname = str(topic.starter)

    if not topic.starter.profile.image:
        uimageurl = '/static/img/default.png'
    else:
        uimageurl = topic.starter.profile.image.url

    if topic.feeling == 'happy':
        ufeeling_url = '/static/img/happy.png'
    else:
        ufeeling_url = '/static/img/angry.png'

    ucat = str(topic.board)
    usubcat = topic.subcategory
    uquick = topic.quick_review
    if uquick == "":
        uquick = "No quick review"
    ubno = topic.bus_no
    udata = str(topic.incident_date)
    utime = str(topic.incident_time)
    urno = topic.route_no
    urname = topic.route_name
    uoperator = topic.bus_operator
    usubject = topic.subject
    ucomment = topic.message

    posts = Post.objects.filter(topic=topic_id)
    html_tag=""""""
    cnt_comment = len(posts)
    ucat_id = topic.category
    for post in posts:

        if post.created_by.profile.image:
            profile_url=post.created_by.profile.image.url
        else:
            profile_url = '/static/img/default.png'
        html_tag += """<li>
            <div class="usercommentinfo-wrapper d-flex flex-row justify-content-between">
                <div class="d-flex flex-row">
                    <img class="avatar-img" src="""""+ profile_url +""" style="border-radius: 50%;">
                    <div class="d-flex flex-column ml-10">
                        <span class="username">Username:</span>
                        <span>"""+'@'+post.created_by.username+"""</span>
                    </div>
                </div>
                <div class="d-flex flex-column" style="width: 160px;">
                    <span class="comment-title" style="overflow:hidden;text-overflow:ellipsis;">"""+post.message+"""</span>
                    <span class="comment-reply">Reply</span>
                </div>
                
                <div class="follow-info up">
                    <img class="heart-img" src='/static/img/love.png' style="max-height:20px;">
                </div>
                <div class="count" style="margin:10px;">"""+str(post.vote)+"""</div>
                <input class="postClass" type='hidden' value='"""+str(post.id)+"""'>
                <div class="follow-info down">
                    <img class="heart-img" src='/static/img/hate.png' style="max-height:20px;">
                </div>
            </div>
        </li>"""

    data = {
        'uname':uname,
        'uimageurl': uimageurl,
        'mfilelist':mfilelist,
        'ufeeling_url':ufeeling_url,
        'ucat':ucat,
        'usubcat':usubcat,
        'uquick':uquick,
        'ubno':ubno,
        'udata':udata,
        'utime':utime,
        'urno':urno,
        'urname':urname,
        'uoperator':uoperator,
        'usubject':usubject,
        'ucomment':ucomment,
        'html_tag':html_tag,
        'cnt_comment':cnt_comment,
        'ucat_id':ucat_id,
    }

    return JsonResponse(data)

def popular(request):
    if request.method == 'POST':
        print('yes')

    return render(request, 'popular.html')

@login_required
def mynotification(request):
    return render(request, 'mynotification.html')

