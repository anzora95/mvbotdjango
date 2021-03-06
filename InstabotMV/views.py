from django.shortcuts import render, redirect
from django.core import serializers

from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import *
from InstabotMV.models import Creds, List_Tag, Media,HashtagList
from .forms import LoginForm, CreateUserForm, TaglistForm, UserlistForm, ComboTagHijo
from InstabotMV.forms import InstaCredsForm

from django.views.generic import View, DetailView, TemplateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
# *************************************************Bot imports**********************************************************

import time

from InstabotMV.src.instabot import InstaBot
from InstabotMV.src.check_status import check_status
from InstabotMV.src.feed_scanner import feed_scanner
from InstabotMV.src.follow_protocol import follow_protocol
from InstabotMV.src.unfollow_protocol import unfollow_protocol
from InstabotMV.forms import ComboTagHijo


import datetime
import logging
import random
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import FormView
from django.shortcuts import redirect

from .forms import GenerateRandomUserForm
from InstabotMV.task import create_random_user_accounts,imprimir,runbot

class GenerateRandomUserView(FormView):
    template_name = 'generate_random_users.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delay(total)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return redirect('users_list')

def pruebaimpresion(self):
    imprimir.delay()
    return redirect('instabot:dashboard')
aux=1

# ****************************************************General***********************************************************

def hastagform(request):
    form =ComboTagHijo()
    return render(request, 'includes/audience/hashtags.html',{'form':form})

def hashtag_read(request):
    if request.method =="POST":
            form= ComboTagHijo(request.POST)
            response = ''
            for key, value in request.POST.items():
                response +='key:%s value:%s\n' %(key, value)
                return HttpResponse(response)
    else:
            form= ComboTagHijo(request) #hacemos el formulario en blanco

    return render(request,'includes/audience/hashtags.html',{'form':form})


def tag_child(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        task =Task()#inicializacion de task
        task.user=user#Se le asigna un usuario a la task
        task.save()

        return redirect('instabot:dashload')

    else:
       return redirect('create.html')

def CreateTask(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        task = Task()  # inicializacion de task
        task.user = user  # Se le asigna un usuario a la task
        task.save()

        return redirect('instabot:dashload')

class ShowView(DetailView):
    model = User
    template_name = 'show.html'
    slug_field = 'username'
    slug_url_kwarg = 'username_url'


class LoginView(View):
    form = LoginForm()
    message = None
    template = "login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('instabot:dashboard')
        return render(request, self.template, self.get_context())

    def post(self, request, *args, **kwargs):
        username_post = request.POST['username']
        password_post = request.POST['password']
        user = authenticate(username=username_post, password=password_post)
        print(user)
        if user.is_superuser == 1:
            login_django(request, user)
            return redirect('instabot:dashboard')
        elif user.is_superuser == 0:
            login_django(request, user)
            return redirect('instabot:dashboard')
        else:
            self.message = "Username o password incorrectos"

        return render(request, self.template, self.get_context())

    def get_context(self):
        return {'form': self.form, 'message': self.message}


@login_required(login_url='instabot:login')
def logout(request):
    logout_django(request)
    return redirect('instabot:login')

def DashboardView(request):
    user = User.objects.get(id=request.user.id) #Get the current user logged in
    ll=LastLogin.objects.get(user=user)
    cred=ll.cred
    AT=Task.objects.all() #Get All the Task in system
    LT=[] ##Empty list for List of Task
    for x in range(0,len(AT)):
       if AT[x].creds==cred:#If the task has the current logged user add it to the LT list
           #print(AT[x].user.username)
           LT.append(AT[x])

    return render(request, 'dashboard.html', {'ll':ll,'LT':LT})

def changeAccount(request,cred):
    user = User.objects.get(id=request.user.id)
    ll=LastLogin.objects.get(id=user.id)
    credex= Creds.objects.get(id=cred)
    ll.cred=credex
    ll.save()
    return redirect('instabot:dashboard')




class DashTaskLoad(LoginRequiredMixin, View):  #vista que servira para redireccionar la task guardada en new task excepto paara los unfollows

    login_url = 'instabot:login'

    def get(self, request, *args, **kwargs):

        context = {
            'user': request.user
            }

        return render(request, 'dashboard.html', context)


class DashboardClient(LoginRequiredMixin, View):
    login_url = 'instabot:login'

    def get(self, request, *args, **kwargs):

        return render(request, 'users/botDashboardClient.html')


class UsersView(LoginRequiredMixin, View):
    login_url = 'instabot:login'

    def get(self, request, *args, **kwargs):
        users_in_system = User.objects.filter(is_superuser=0)

        context = {
            'users': users_in_system
        }

        return render(request, 'admin/clients.html', context)


class UserAccounts(LoginRequiredMixin, View):
    login_url = 'instabot:login'
    template_name = 'users/mybot.html'
    
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id) #Get the current user logged in
        ll=LastLogin.objects.get(user=user)
        cred=ll.cred
        user=User.objects.get(id=request.user.id) #Obtencion del usuario logeado
        creds = Creds.objects.all() #Obtencion de todas las credenciales 
        lcreds=[] #Inicializacion de lista de credenciales
        for x in range(0,len(creds)):
            if creds[x].user==user:
                lcreds.append(creds[x])

        
        
        return render(request, 'users/mybot.html', {'lcreds':lcreds,'ll':ll})

    def post(self, request):
        user = User.objects.get(id=request.user.id) #Get the current user logged in
        ll=LastLogin.objects.get(user=user)
        cred=ll.cred
        if request.method == 'POST':
            user=User.objects.get(id=request.user.id) # Se toma el usuario django que eta logeado.
            cred = Creds()  # inicializacion de Credentials
            cred.user = user  # Se le asigna un usuario a la task
            cred.insta_user=request.POST.get('insta_user')
            cred.insta_pass=request.POST.get('insta_pass')
            cred.save()
            return redirect('instabot:userAccounts')
        
        return redirect('instabot:dashboard')


def NewTask(request):
    user = User.objects.get(id=request.user.id) #Get the current user logged in
    ll=LastLogin.objects.get(user=user)
    cred=ll.cred
    return render(request, 'tasks/newTask.html', {'ll':ll})
import json
def tags(request,id_tag):

    tags= List_Tag.objects.filter(category=id_tag)
    qs_json=serializers.serialize('json', tags)
    return HttpResponse(qs_json,content_type='application/json')
class hashtags(TemplateView):

    def get(self, request, *args, **kwargs):
        idTag= request.GET['id']
        tags = List_Tag.objects.filter(category=idTag)
        data = serializers.serialize('json',tags,fields=('insta_tag','category'))
        print(data)
        return HttpResponse(data,content_type='application/json')

def tags_serializer(tag):
    return {'id':tag.id,'name':tag.insta_tag}

def GetHashtags(request):
    category=request.GET.get('category')
    tags = List_Tag.objects.get(category=category)
    qs_json = serializers.serialize('json', tags)

    return HttpResponse(qs_json, content_type='application/json')


def TrueOrFalse(data):
    if data=='on':

        return True
    else:

        return False

def DeleteTask(request, id_task):
    if request.method == 'POST':
        task=Task.objects.get(id=id_task)
        task.delete()
        return redirect('instabot:dashboard')
    return render(request,'tasks/del_task.html')

def NewFollowLike(request):
    Hasgtags = HashtagList.objects.all()
    user = User.objects.get(id=request.user.id)
    ll=LastLogin.objects.get(user=user)
    cred=ll.cred
    if request.method == 'POST':
        task = Task()  # inicializacion de task
        task.user = user  # Se le asigna un usuario a la task
        task.creds=cred
        task.tags=request.POST.get('tags-input')
        task.active = False
        task.likemedia=TrueOrFalse(request.POST.get('like'))
        task.followuser=TrueOrFalse(request.POST.get('follow'))
        task.dontlikemedia=TrueOrFalse(request.POST.get('dont'))
        task.dontfollow=TrueOrFalse(request.POST.get('dontfollow'))
        task.randomlylike=TrueOrFalse(request.POST.get('randomly'))
        task.search=TrueOrFalse(request.POST.get('search'))
        task.antispamfilter=TrueOrFalse(request.POST.get('antispam'))
        task.custowordfilter=TrueOrFalse(request.POST.get('custom'))
        task.save()
        return redirect('instabot:dashboard')
    return render(request, 'tasks/followAndLike.html', {'Hasgtags': Hasgtags,'ll':ll})

class UnfollowTask(LoginRequiredMixin,View):
    def get(self,request, *args, **kwargs):
        return render(request,'tasks/unfollow_task.html',{})

# **************************************************Bot****************************************************************


class StoreTask(LoginRequiredMixin, TemplateView):  # view para los hastag para ser targetados en las nuevas task
    template_name = 'includes/audience/hashtags.html'
    login_url = 'instabot:login'
    model = List_Tag

    def post(self, request):
        form = TaglistForm(request.POST)

        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()

            return redirect('instabot:dashboard')

        args = {'form': form}

        return render(request, self.template_name, args)


class StoreTaskUser(LoginRequiredMixin, TemplateView):  #view para los user a ser targeteados en las nuevas task
    template_name = 'includes/audience/friendList.html'
    login_url = 'instabot:login'
    model = List_Tag

    def post(self, request):
        form = UserlistForm(request.POST)

        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()

            return redirect('instabot:dashboard')

        args = {'form': form}

        return render(request, self.template_name, args)


class StoreTaskLocations(LoginRequiredMixin, TemplateView):  #view Para las locationsa ser targeteados pestaña de locations en las nueva task
    template_name = 'includes/audience/location.html'
    login_url= 'instabot:login' #Este boton de redireccionamiento debe estar hasta abajo con uno de retroceso 
    model = List_Tag

    def post(self, request):
        pass

class StartBot(LoginRequiredMixin, View):
    login_url = 'instabot:login'

    def get(self, request, *args, **kwargs):

        return render(request, 'users/dashboard.html', {})

    def post(self, request, *args, **kwargs):
        user=User.objects.get(id=request.user.id)
        ll=LastLogin.objects.get(user=user)
        cred=Creds.objects.get(id=ll.cred.id)
        print(task)
        user=User.objects.get(id=request.user.id)
        bot = InstaBot(
            login=cred.insta_user,
            password=cred.insta_pass,
            like_per_day=1000,
            comments_per_day=0,
            tag_list=['mac4life','macbook'],
            tag_blacklist=['rain', 'thunderstorm'],
            user_blacklist={},
            max_like_for_one_tag=50,
            follow_per_day=300,
            follow_time=1 * 120,
            unfollow_per_day=300,
            unfollow_break_min=15,
            unfollow_break_max=30,
            log_mod=0,
            proxy='',
            # Lista de palabras de las cuales se generarán los comentarios
            # For example: "This shot feels wow!"
            comment_list=[["this", "the", "your"],
                          ["photo", "picture", "pic", "shot", "snapshot"],
                          ["is", "looks", "feels", "is really"],
                          ["great", "super", "good", "very good", "good", "wow",
                           "WOW", "cool", "GREAT", "magnificent", "magical",
                           "very cool", "stylish", "beautiful", "so beautiful",
                           "so stylish", "so professional", "lovely",
                           "so lovely", "very lovely", "glorious", "so glorious",
                           "very glorious", "adorable", "excellent", "amazing"],
                          [".", "..", "...", "!", "!!", "!!!"]],
            # Use unwanted_username_list to block usernames containing a string
            ## Will do partial matches; i.e. 'mozart' will block 'legend_mozart'
            ### 'free_followers' will be blocked because it contains 'free'
            unwanted_username_list=[
                'second', 'stuff', 'art', 'project', 'love', 'life', 'food', 'blog',
                'free', 'keren', 'photo', 'graphy', 'indo', 'travel', 'art', 'shop',
                'store', 'sex', 'toko', 'jual', 'online', 'murah', 'jam', 'kaos',
                'case', 'baju', 'fashion', 'corp', 'tas', 'butik', 'grosir', 'karpet',
                'sosis', 'salon', 'skin', 'care', 'cloth', 'tech', 'rental', 'kamera',
                'beauty', 'express', 'kredit', 'collection', 'impor', 'preloved',
                'follow', 'follower', 'gain', '.id', '_id', 'bags'
            ],
            unfollow_whitelist=['example_user_1', 'example_user_2'])
        while True:

            # print("# MODE 0 = ORIGINAL MODE BY LEVPASHA")
            # print("## MODE 1 = MODIFIED MODE BY KEMONG")
            # print("### MODE 2 = ORIGINAL MODE + UNFOLLOW WHO DON'T FOLLOW BACK")
            # print("#### MODE 3 = MODIFIED MODE : UNFOLLOW USERS WHO DON'T FOLLOW YOU BASED ON RECENT FEED")
            # print("##### MODE 4 = MODIFIED MODE : FOLLOW USERS BASED ON RECENT FEED ONLY")
            # print("###### MODE 5 = MODIFIED MODE : JUST UNFOLLOW EVERYBODY, EITHER YOUR FOLLOWER OR NOT")

            ################################
            ##  WARNING   ###
            ################################

            # DON'T USE MODE 5 FOR A LONG PERIOD. YOU RISK YOUR ACCOUNT FROM GETTING BANNED
            ## USE MODE 5 IN BURST MODE, USE IT TO UNFOLLOW PEOPLE AS MANY AS YOU WANT IN SHORT TIME PERIOD

            mode = 0

            # print("You choose mode : %i" %(mode))
            # print("CTRL + C to cancel this operation or wait 30 seconds to start")
            # time.sleep(30)

            if mode == 0:
                bot.new_auto_mod()


            elif mode == 1:
                check_status(bot)
                while bot.self_following - bot.self_follower > 200:
                    unfollow_protocol(bot)
                    time.sleep(10 * 60)
                    check_status(bot)
                while bot.self_following - bot.self_follower < 400:
                    while len(bot.user_info_list) < 50:
                        feed_scanner(bot)
                        time.sleep(5 * 60)
                        follow_protocol(bot)
                        time.sleep(10 * 60)
                        check_status(bot)

            elif mode == 2:
                bot.bot_mode = 1
                bot.new_auto_mod()
                media=Media.objects.All().OrderBy('datetime')


            elif mode == 3:
                unfollow_protocol(bot)
                time.sleep(10 * 60)

            elif mode == 4:
                feed_scanner(bot)
                time.sleep(60)
                follow_protocol(bot)
                time.sleep(10 * 60)

            elif mode == 5:
                bot.bot_mode = 2
                unfollow_protocol(bot)
                media=Media.objects.All().OrderBy('datetime')


            else:
                print("Wrong mode!")

        return render(request, 'dashboard.html', {})


def start(request, task):
    user=User.objects.get(id=request.user.id)
    ll=LastLogin.objects.get(user=user)
    cred=Creds.objects.get(id=ll.cred.id)
    u=cred.insta_user
    p=cred.insta_pass
    task=Task.objects.get(id=task)
    if task.active:
        task.active=False
    else:
        task.active=True
    task.save()
    strtask=task.tags
    hl=strtask.split(",")
    print(hl)
    user=User.objects.get(id=request.user.id)
    runbot.delay(u,p,hl)
    return redirect('instabot:dashboard')

class StopBot(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html', {})

    def post(self):
        url_logout = 'https://www.instagram.com/accounts/logout/'

        now_time = datetime.datetime.now()
        log_string = 'Logout: likes - %i, follow - %i, unfollow - %i, comments - %i.' % \
                        (self.like_counter, self.follow_counter,
                        self.unfollow_counter, self.comments_counter)
        self.write_log(log_string)
        work_time = datetime.datetime.now() - self.bot_start
        log_string = 'Bot work time: %s' % (work_time)
        self.write_log(log_string)

        try:
            logout_post = {'csrfmiddlewaretoken': self.csrftoken}
            logout = self.s.post(self.url_logout, data=logout_post)
            self.write_log("Logout success!")
            self.login_status = False
        except:
            logging.exception("Logout error!")

    def cleanup(self, *_): #proceso de unfollow  para los task de unfollow
        # Unfollow all bot follow
        if self.follow_counter >= self.unfollow_counter:
            for f in self.bot_follow_list:
                log_string = "Trying to unfollow: %s" % (f[0])
                self.write_log(log_string)
                self.unfollow_on_cleanup(f[0])
                sleeptime = random.randint(self.unfollow_break_min,
                                            self.unfollow_break_max)
                log_string = "Pausing for %i seconds... %i of %i" % (
                    sleeptime, self.unfollow_counter, self.follow_counter)
                self.write_log(log_string)
                time.sleep(sleeptime)
                self.bot_follow_list.remove(f)

        # Logout
            if self.login_status:
                self.logout()
        return redirect('instabot:dashboard')


class MyBot(LoginRequiredMixin, TemplateView):
    template_name = 'users/mybot.html'
    login_url = 'instabot:login'
    model = Creds

    def get(self, request, **kwargs):
        creds = Creds.objects.filter(user_id=request.user)
        form = InstaCredsForm()
        context = super(MyBot, self).get_context_data(**kwargs)

        if creds is not None:
            return render(request, 'users/startBot.html')

        return render(request, self.template_name, context, {'form': form})

    def post(self, request):
        form = InstaCredsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            return redirect('instabot:start')

        args = {'form': form,
                'text': text}
        return render(request, self.template_name, args)


class CommentList(LoginRequiredMixin, TemplateView):
    template_name = 'users/comments.html'
    login_url = 'instabot:login'

    def get(self, request, *args, **kwargs):
        return render(request, 'users/comments.html', {})


class BlackList(LoginRequiredMixin, TemplateView):
    template_name = 'users/blackList.html'
    login_url = 'instabot:login'

    def get(self, request, *args, **kwargs):
        return render(request, 'users/blackList.html', {})


class Create(LoginRequiredMixin, TemplateView):
    template_name = 'includes/dialog.html'
    login_url = 'instabot:login'
    model = Creds, User

    def post(self, request):
        form = CreateUserForm(request.POST)
        form2 = InstaCredsForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

        if form2.is_valid():
            post = form2.save(commit=False)
            post.user = request.user
            post.save()

            return redirect('instabot:user-list')

        args = {'form': form,
                'form2': form2}

        return render(request, self.template_name, args)

# **********************************************User Options************************************************************

class Profile(LoginRequiredMixin, View):
    model = User
    login_url = 'instabot:login'

    def get(self, request, *args, **kwargs):
        context = {'user': request.user}
        return render(request, 'users/account.html', context)


class ManageUsers(LoginRequiredMixin, View):
    model = User, Creds
    login_url = 'instabot:login'

    def get(self, request, user_id):
        user_in_system = User.objects.get(id=user_id)

        context = {'u_system': user_in_system}

        return render(request, 'admin/manageAccount.html', context)


class UserUpdate(UpdateView):
    model = User
    form_class = CreateUserForm
    template_name = 'users/accountedit.html'
    success_url = reverse_lazy('instabot:user-list')


class UserDelete(DeleteView):
    model = User
    template_name = 'users/accountedit.html'
    success_url = reverse_lazy('instabot:user-list')



class MediaList(ListView):
    model=Media
    template_name = 'dashboard.html'

