from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from users.models import meetia_user
from campaigns.models import Campaign
from users.models import message
from users.models import PasswordToken
import random
import string
from django.db import IntegrityError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import HttpResponse




def homepage(request):
    groups = Campaign.objects.all()
    return render(request, 'home.html', {
        'groups': groups
    })


def signin_user(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            error_message = 'ایمیل یا رمز عبور اشتباه است!'
            return render(request, 'login.html', {'error_message': error_message})
    if request.method == "GET":
        return render(request, 'login.html', {
        })


def signup_user(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    if request.method == "POST":
        try:
            first_name = request.POST.get('first-name')
            last_name = request.POST.get('last-name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password,
                                        username=email)
            meetia_user.objects.create(user=user)
            user.save()
            return HttpResponseRedirect("/signin/")
        except IntegrityError:
            duplicate_key = 'این ایمیل قبلا ثبت شده.'
            return render(request , 'signup.html' , {
                'duplicate_key' : duplicate_key
            })

def user_profile(request, user_id):
    if request.method == "GET":
        user = User.objects.get(id=user_id)
        m_user = meetia_user.objects.get(user=user)
        return render(request, 'userprofile.html', {
            'user': user, 'meetia_user': m_user
        })


@login_required(login_url='/signin/')
def edit_personalinfo(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "GET":
        if user == request.user:
            return render(request, 'profile.html', {
                'user': user
            })
        else:
            return render(request, 'userprofile.html')
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        if request.user == user:
            user.first_name = request.POST.get('first-name')
            user.last_name = request.POST.get('last-name')
            user.email = request.POST.get('email')
            user.username = request.POST.get('email')
            user.save()
            return HttpResponseRedirect("/profile/" + user.id.__str__())
        else:
            return HttpResponseRedirect("/profile/" + user.id.__str__())


@login_required(login_url='/signin/')
def edit_password(request, user_id):
    if request.method == "GET":
        user = User.objects.get(id=user_id)
        if request.user == user:
            return render(request, 'changepassword.html', {
                'user': user
            })
        else:
            return render(request, 'userprofile.html', {
                'user': user
            })
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        if request.user == user:
            new_password = request.POST.get('new-password')
            user.set_password(new_password)
            user.save()
            return HttpResponseRedirect("/signin/")
        else:
            return HttpResponseRedirect("/profile/" + user.id.__str__())


@login_required(login_url='/signin/')
def profile_picture(request, user_id):
    if request.method == "GET":
        user = User.objects.get(id=user_id)
        if request.user == user:
            return render(request, 'profilepicture.html', {'user': user})
        else:
            return render(request, 'userprofile.html', {'user': user})
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        if request.user == user:
            picture = request.FILES.get('profile_picture')
            user = request.user
            m_user = meetia_user.objects.get(user=user)
            m_user.profile_picture = picture
            m_user.save()
            return HttpResponseRedirect("/profile/" + user.id.__str__())
        else:
            return HttpResponseRedirect("/profile/" + user.id.__str__())


@login_required(login_url='/signin/')
def user_groups(request, user_id):
    if request.method == "GET":
        user = User.objects.get(id=user_id)
        if request.user == user:
            return render(request, 'managemygroups.html', {'user': user})
        else:
            return HttpResponseRedirect("/profile/" + user.id.__str__())


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def rules(request):
    if request.method == "GET":
        return render(request, 'rules.html')


def about_us(request):
    if request.method == "GET":
        return render(request, 'aboutus.html')


def what_is_meetia(request):
    if request.method == "GET":
        return render(request, 'whatismeetia.html')


@login_required(login_url='/signin/')
def new_message(request, user_id):
    sender = request.user
    receiver = User.objects.get(id=user_id)
    if request.method == "GET":
        return render(request, 'newmessage.html', {
            'receiver': receiver,
        })
    if request.method == "POST":
        content = request.POST.get("content")
        message.objects.create(receiver=receiver, sender=sender, content=content)
        return HttpResponseRedirect("/profile/" + sender.id.__str__())


def my_messages(request, user_id):
    user = User.objects.get(id=user_id)
    if request.user == user:
        if request.method == "GET":
            all_messages = message.objects.all()
            my_messages = all_messages.filter(receiver=request.user)
            return render(request, 'messages.html', {
                'my_messages': my_messages
            })
    else:
        return HttpResponseRedirect("/profile/" + user.id.__str__())


def sent_messages(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "GET":
        if request.user == user:
            all_messages = message.objects.all()
            my_messages = all_messages.filter(sender=request.user)
            return render(request, 'sentmessages.html', {
                'my_messages': my_messages
            })
        else:
            return HttpResponseRedirect('/profile/' + user.id.__str__())


def email_password_token(request):
    if request.method == "GET":
        return render(request, 'forgotpassword.html')
        # Return email for forget password shit
    elif request.method == "POST":
        if request.POST.get("email", None):
            current_user = User.objects.filter(email=request.POST['email'])
            if current_user:
                current_user = current_user[0]
                if not PasswordToken.objects.filter(user=current_user):
                    token = generate_random_token()
                    token_obj = PasswordToken.objects.create(user=current_user, token=token)
                    email = request.POST.get("email")
                    subject = 'میتیا - فراموشی رمز عبور'
                    html_content = render_to_string('forgot_password_email.html' , {
                        'token_obj' : token_obj
                    })
                    text_content = strip_tags(html_content)
                    mail = EmailMultiAlternatives(subject , text_content ,'' , [email])
                    mail.attach_alternative(html_content ,"text/html" )
                    mail.send()
                    success = 'ایمیل با موفقیت ارسال شد.'
                    return render(request, 'forgotpassword.html', {
                        'success': success
                    })
                else:
                    token_obj = PasswordToken.objects.get(user=current_user)
                    email = request.POST.get("email")
                    subject = 'میتیا - فراموشی رمز عبور'
                    html_content = render_to_string('forgot_password_email.html' , {
                        'token_obj' : token_obj
                    })
                    text_content = strip_tags(html_content)
                    mail = EmailMultiAlternatives(subject , text_content ,'' , [email])
                    mail.attach_alternative(html_content ,"text/html" )
                    mail.send()
                    success = 'ایمیل با موفقیت ارسال شد.'
                    return render(request, 'forgotpassword.html', {
                        'success': success
                    })
            else:
                fail = 'ایمیل وارد شده صحیح نیست!'
                return render(request, 'forgotpassword.html', {
                    'fail': fail
                })
        else:
            fail = 'ایمیل وارد شده صحیح نیست!'
            return render(request, 'forgotpassword.html', {
                'fail': fail
            })


def change_password(request):
    if request.method == "GET":
        token = request.GET['token']
        return render(request, 'passwordreset.html', {
            'token' : token
        } )
    elif request.method == "POST":
        if request.GET.get("token", None):
            token = request.GET['token']
            if PasswordToken.objects.filter(token=token):
                password_token_user = PasswordToken.objects.get(token=token).user
                password_token_user.set_password(request.POST['password'])
                password_token_user.save()
                pass_changed_success = 'تغییر رمز عبور با موفقیت انجام شد.'
                return render(request, 'passwordreset.html', {
                    'pass_changed_success' : pass_changed_success
                })
            else:
                token_invalid = 'لینک شما معتبر نیست!'
                return render(request, 'passwordreset.html', {
                    'token_invalid': token_invalid , 'token' : token
                })
        else:
            invalid_link = 'لینک شما معتبر نیست.'
            return render(request , 'passwordreset.html' , {
                'invalid_link' : invalid_link
            })



def passwords_valid(request):
    pass


def generate_random_token():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))


def no_brakes_on_development_train(request):
    if request.method == "POST":
        user_idea = request.POST.get('user_idea')
        user = request.user.username
        send_mail(user, user_idea, '', ['salam@meetia.ir'])
        success_message = 'نظر شما با موفقیت ثبت شد!'
        return render(request, 'idea_sent.html', {
            'success_message': success_message
        })
    if request.method == "GET":
        return render(request, 'idea_sent.html')



def jashnvare_verify(request) :
    return HttpResponse("2970085")
