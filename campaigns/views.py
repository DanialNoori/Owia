from django.shortcuts import render
from campaigns.models import Campaign
from campaigns.models import Meeting
from campaigns.models import group_album
from campaigns.models import group_posts
from campaigns.models import group_posts_comments
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from PIL import Image


@login_required(login_url='/signin/')
def create_group(request):
    if request.method == "POST":
        group_image = request.FILES.get('group_image')
        group_description = request.POST.get('group_description')
        group_name = request.POST.get('group_name')
        group = Campaign.objects.create(group_description=group_description, group_name=group_name,
                                        group_image=group_image, group_owner=request.user)
        group.group_listofmembers.add(request.user)
        return HttpResponseRedirect("/groups/" + group.id.__str__())
    if request.method == "GET":
        return render(request, 'creategroup.html')


@login_required(login_url='/signin/')
def edit_group(request, group_id):
    if request.method == "GET":
        group = Campaign.objects.get(id=group_id)
        return render(request, 'editgroup.html', {
            'group': group
        })
    if request.method == "POST":
        group = Campaign.objects.get(id=group_id)
        uploaded_image = request.FILES.get('group_image')
        group.group_description = request.POST.get('group_description')
        group.group_name = request.POST.get('group_name')
        if uploaded_image:
            group.group_image = uploaded_image
            group.save()
            return HttpResponseRedirect("/groups/" + group.id.__str__())
        else:
            group.save()
            return HttpResponseRedirect("/groups/" + group.id.__str__())

def all_campaigns(request):
    if request.method == "GET":
        campaigns = Campaign.objects.all()
        return render(request, 'groups.html', {
            'campaigns': campaigns
        })


def group_page(request, group_id):
    if request.method == "GET":
        group = Campaign.objects.get(id=group_id)
        owner = group.group_owner
        listofmembers = group.group_listofmembers
        return render(request, 'grouppage.html', {
            'group': group, 'group_owner': owner, 'group_listofmembers': listofmembers
        })

    if request.method == "POST":  # joining the group
        user = request.user
        group = Campaign.objects.get(id=group_id)
        listofmembers = group.group_listofmembers
        if user.is_authenticated():
            if user in group.group_listofmembers.all():
                listofmembers.remove(user)
                group.group_members -= 1
                group.save()
                return HttpResponseRedirect("/groups/" + group.id.__str__())

            else:
                group = Campaign.objects.get(id=group_id)
                group.group_listofmembers.add(user)
                group.group_members += 1
                group.save()
                return HttpResponseRedirect("/groups/" + group.id.__str__())
        else:
            return HttpResponseRedirect('/signin/')


@login_required(login_url='/signin/')
def group_meetings(request, group_id):
    if request.method == "GET":
        group = Campaign.objects.get(id=group_id)
        all_meetings = Meeting.objects.all()
        my_meetings = all_meetings.filter(meeting_group=group)
        if request.user in group.group_listofmembers.all():
            return render(request, 'groupmeetings.html', {
                'group': group, 'my_meetings': my_meetings
            })
        else:
            return HttpResponseRedirect("/groups/" + group.id.__str__())


def meeting_page(request, meeting_id, group_id):
    group = Campaign.objects.get(id=group_id)
    meeting = Meeting.objects.get(id=meeting_id)
    if request.method == "GET":
        return render(request, 'meetingpage.html', {
            'group': group, 'meeting': meeting
        })
    if request.method == "POST":
        if request.user in meeting.who_is_coming.all():
            user = request.user
            meeting.who_is_coming.remove(user)
            return HttpResponseRedirect("/groups/group-meetings/" + group.id.__str__() + '/' + meeting.id.__str__())
        else:
            user = request.user
            meeting.who_is_coming.add(user)
            return HttpResponseRedirect("/groups/group-meetings/" + group.id.__str__() + '/' + meeting.id.__str__())

@login_required(login_url='/signin/')
def new_meeting(request, group_id):
    if request.method == "GET":
        group = Campaign.objects.get(id=group_id)
        owner = group.group_owner
        if request.user in group.group_listofmembers.all():
            if request.user == owner:
                return render(request, 'newmeeting.html', {
                    'group': group
                })
            else:
                return HttpResponseRedirect("/groups/group-meetings/" + group.id.__str__())

        else:
            return HttpResponseRedirect("/groups/" + group.id.__str__())

    if request.method == "POST":
        group = Campaign.objects.get(id=group_id)
        meeting_location = request.POST.get('meeting_location')
        meeting_date = request.POST.get('meeting_date')
        meeting_name = request.POST.get('meeting_name')
        meeting_description = request.POST.get('meeting_description')
        Meeting.objects.create(meeting_date=meeting_date, meeting_description=meeting_description,
                               meeting_location=meeting_location
                               , meeting_name=meeting_name, meeting_group=group)
        return HttpResponseRedirect("/groups/group-meetings/" + group.id.__str__())


def edit_meeting(request , group_id ,meeting_id ):
        group = Campaign.objects.get(id=group_id)
        meeting = Meeting.objects.get(id=meeting_id)
        if request.method == "GET":
            if request.user == group.group_owner:
                return render(request , 'editmeeting.html' , {
                'group' : group , 'meeting' : meeting
            })
            else:
                return HttpResponseRedirect("/groups/group-meetings/" + group.id.__str__() + meeting.id.__str__())
        if request.method == "POST":
            if request.user == group.group_owner:
                meeting.meeting_name = request.POST.get("meeting_name")
                meeting.meeting_location = request.POST.get("meeting_location")
                meeting.meeting_description = request.POST.get("meeting_description")
                meeting.meeting_date = request.POST.get("meeting_date")
                meeting.save()
                return HttpResponseRedirect("/groups/group-meetings/" + group.id.__str__() + '/' + meeting.id.__str__())
            else:
                return HttpResponseRedirect("/groups/group-meetings/" + group.id.__str__() + meeting.id.__str__())

@login_required(login_url='/signin/')
def group_pictures(request, group_id):
    if request.method == "GET":
        group = Campaign.objects.get(id=group_id)
        all_pictures = group_album.objects.all()
        my_pictures = all_pictures.filter(group=group)
        if request.user in group.group_listofmembers.all():
            return render(request, 'grouppictures.html', {
                'group': group, 'my_pictures': my_pictures
            })
        else:
            return HttpResponseRedirect("/groups/" + group.id.__str__())

    if request.method == "POST":
        all_pictures = group_album.objects.all()
        group = Campaign.objects.get(id=group_id)
        my_pictures = all_pictures.filter(group=group)
        new_group_picture = request.FILES.get('group_picture_new')
        try:
            new_group_picture.verify()
            group = Campaign.objects.get(id=group_id)
            group_album.objects.create(pictures=new_group_picture, group=group)
            return HttpResponseRedirect("/groups/group-pictures/" + group.id.__str__())
        except:
            no_image_uploaded = 'آپلود این فایل امکان پذیر نیست.'
            return render(request, 'grouppictures.html', {
                'no_image_uploaded': no_image_uploaded, 'group': group, 'my_pictures': my_pictures
            })


@login_required(login_url='/signin/')
def group_members(request, group_id):
    if request.method == "GET":
        group = Campaign.objects.get(id=group_id)
        if request.user in group.group_listofmembers.all():
            meetia_users_of_group = group.group_listofmembers.all()
            return render(request, 'groupmembers.html', {
                'group': group, 'meetia_user_of_group': meetia_users_of_group
            })
        else:
            meetia_users_of_group = group.group_listofmembers.all()
            return render(request, 'groupmembers.html', {
                'group': group, 'meetia_user_of_group': meetia_users_of_group
            })


def groups(request):
    if request.method == "GET":
        groups = Campaign.objects.all()
        return render(request, 'groups.html', {
            'groups': groups
        })


def group_discussions(request, group_id):
    if request.method == "GET":
        group = Campaign.objects.get(id=group_id)
        posts = group_posts.objects.filter(group=group)
        return render(request, 'groupdiscussions.html', {
            'group': group, 'posts': posts
        })


def post_page(request, group_id, post_id):
    if request.method == "GET":
        group = Campaign.objects.get(id=group_id)
        post = group_posts.objects.get(id=post_id)
        comments = group_posts_comments.objects.filter(comment_for_post=post)
        return render(request, 'postpage.html', {
            'group': group, 'post': post, 'comments': comments
        })
    if request.method == "POST":
        group = Campaign.objects.get(id=group_id)
        post = group_posts.objects.get(id=post_id)
        comment_writer = request.user
        comments = request.POST.get('comment')
        group_posts_comments.objects.create(comments=comments, comment_writer=comment_writer, comment_for_post=post)
        return HttpResponseRedirect('/groups/group-discussions/' + group.id.__str__() + "/" + post.id.__str__())


def post_edit(request, group_id, post_id):
    post = group_posts.objects.get(id=post_id)
    group = Campaign.objects.get(id=group_id)
    if request.user == post.post_writer:
        if request.method == "GET":
            return render(request, "editpost.html", {
            'group': group, 'post': post
        })
        if request.method == "POST":
            post.posts = request.POST.get('post')
            post.post_title = request.POST.get('post_title')
            post.save()
            return HttpResponseRedirect('/groups/group-discussions/' + group.id.__str__() + "/" + post.id.__str__())
    else:
        return HttpResponseRedirect('/groups/group-discussions/' + group.id.__str__() + "/" + post.id.__str__())

def new_post(request, group_id):
    if request.method == "GET":
        group = Campaign.objects.get(id=group_id)
        return render(request, 'newpost.html', {
            'group': group
        })
    if request.method == "POST":
        group = Campaign.objects.get(id=group_id)
        post_title = request.POST.get('post_title')
        post_writer = request.user
        posts = request.POST.get('post')
        post_to_redirect = group_posts.objects.create(group=group, post_title=post_title, posts=posts,
                                                      post_writer=post_writer)
        return HttpResponseRedirect(
            '/groups/group-discussions/' + group.id.__str__() + "/" + post_to_redirect.id.__str__())
