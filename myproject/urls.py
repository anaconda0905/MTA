from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views
from boards import views
from geoshop import views as test_views

urlpatterns = [
    url(r'^$', accounts_views.home, name='home'),
    url(r'^started$', accounts_views.started, name='get_started'),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^login/$', accounts_views.login_user, {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            html_email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ), 
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
    # url(r'^settings/account/$', accounts_views.UserUpdateView.as_view(), name='my_account'),
    url(r'^settings/account/$', accounts_views.edit_user, name='my_account'),

    url(r'^settings/account/survey/$', accounts_views.data_survey, name='data_survey'),
    url(r'^survey/update$', accounts_views.data_survey_update, name='data_survey_update'),
    url(r'^contactus/$', accounts_views.contactus, name='contactus'),

    url(r'^forum/$', accounts_views.forum, name='forum'),
    url(r'^review/$', views.review, name='review'),

    url(r'^boards/(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),

    url(r'^posts/(?P<post_pk>\d+)/$', views.CommentListView.as_view(), name='post_comments'),

    url(r'^posts/(?P<post_pk>\d+)/reply/$', views.reply_comment, name='reply_comment'),

    url(r'^posts/(?P<post_pk>\d+)/comments/(?P<comment_pk>\d+)/edit/$', views.CommentUpdateView.as_view(), name='edit_comment'),

    url(r'^mapview/$', views.mapview, name='mapview'),
    url(r'^popluar/$', views.popular, name='popular'),
    url(r'^admin/', admin.site.urls),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', accounts_views.activate, name='activate'),
    url(r'^ajax/topicdata/$', views.topicdata, name='topicdata'),
    url(r'^ajax/updatetopicdata/$', views.updatetopicdata, name='updatetopicdata'),
    url('test', test_views.Home.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)