from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^signup/$', 'users.views.signup_user'),
                  url(r'^signin/$', 'users.views.signin_user'),
                  url(r'^logout/$', 'users.views.logout_user'),
                  url(r'^creategroup/$', 'campaigns.views.create_group'),
                  url(r'^$', 'users.views.homepage'),
                  url(r'^campaigns/$', 'campaigns.views.all_campaigns'),
                  url(r'^groups/(?P<group_id>\w+)/$', 'campaigns.views.group_page'),
                  url(r'^groups/edit-group/(?P<group_id>\w+)/$', 'campaigns.views.edit_group'),
                  url(r'^groups/group-meetings/(?P<group_id>\w+)/$', 'campaigns.views.group_meetings'),
                  url(r'^groups/new-meeting/(?P<group_id>\w+)/$', 'campaigns.views.new_meeting'),
                  url(r'^groups/group-meetings/(?P<group_id>\w+)/(?P<meeting_id>\w+)/$',
                      'campaigns.views.meeting_page'),
                  url(r'^groups/group-meetings/(?P<group_id>\w+)/(?P<meeting_id>\w+)/edit/$',
                      'campaigns.views.edit_meeting'),
                  url(r'^groups/(?P<group_id>\w+)/leave/$', 'campaigns.views.group_page'),
                  url(r'^groups/group-discussions/(?P<group_id>\w+)/$', 'campaigns.views.group_discussions'),
                  url(r'^groups/group-pictures/(?P<group_id>\w+)/$', 'campaigns.views.group_pictures'),
                  url(r'^groups/group-members/(?P<group_id>\w+)/$', 'campaigns.views.group_members'),
                  url(r'^groups/group-discussions/(?P<group_id>\w+)/(?P<post_id>\w+)/$', 'campaigns.views.post_page'),
                  url(r'^groups/group-discussions/(?P<group_id>\w+)/(?P<post_id>\w+)/edit/$', 'campaigns.views.post_edit'),
                  url(r'^groups/group-discussions/(?P<group_id>\w+)/new-post/$', 'campaigns.views.new_post'),
                  url(r'^profile/(?P<user_id>\d+)/$', 'users.views.user_profile'),
                  url(r'^profile/edit/(?P<user_id>\d+)/$', 'users.views.edit_personalinfo'),
                  url(r'^profile/change-password/(?P<user_id>\d+)/$', 'users.views.edit_password'),
                  url(r'^profile/profile-picture/(?P<user_id>\d+)/$', 'users.views.profile_picture'),
                  url(r'^profile/new-message/(?P<user_id>\d+)/$', 'users.views.new_message'),
                  url(r'^profile/rstpass/$', 'users.views.change_password'),
                  url(r'^passrecovery/$', 'users.views.email_password_token'),
                  url(r'^profile/user-groups/(?P<user_id>\d+)/$', 'users.views.user_groups'),
                  url(r'^profile/messages/(?P<user_id>\d+)/$', 'users.views.my_messages'),
                  url(r'^profile/messages/(?P<user_id>\d+)/sent/$', 'users.views.sent_messages'),
                  url(r'^groups/$', 'campaigns.views.groups'),
                  url(r'^rules/$', 'users.views.rules'),
                  url(r'^about-us/$', 'users.views.about_us'),
                  url(r'^what-is-meetia/$', 'users.views.what_is_meetia'),
                  url(r'^jashnvare_verify.txt/$', 'users.views.jashnvare_verify'),
                  url(r'^no-brakes-on-development-train/$', 'users.views.no_brakes_on_development_train'),
                  url(r'^test_together/$', 'users.views.test_together')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)