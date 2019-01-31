from InstabotMV.src import InstaBot
from InstabotMV.src.sql_updates import take_cred
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from InstabotMV.src import check_status, follow_protocol, unfollow_protocol,feed_scanner
import time
from InstabotMV.models import Media, ChildTag

#esta seria la nueva vista starbot del dashboard donde al crear el task en la vista anterior de new task enviaria via url los pk del hsahtag padre que se selcciono y para buscar en la tabla hashtag hijo segun su hashtag padre.


class StartBot(LoginRequiredMixin, View):
    login_url = 'instabot:login'

    # esta funcion se ocupara cuando se haya pasado valores (en este caso una pk) en los parametros de una url
    def dats_url(self, form):
        success = super().form_valid(form)  # obtengo los datos de formulario
        # aqui asignas
        hastgs = self.kwargs.get('pk')  # obtengo las pk que vienen en el url
        # luego de esto se usara para crear un query set par buscar esta pk en la bd en la tabla de los hashtags hijo y asi usara esos tags para la busqueda

        query_set = ChildTag.objects.filter(hashtag_id=hastgs)

        # ahora este query set asignarselo a las busquedas de los hashtags

        return query_set

    def get(self, request, *args, **kwargs):

        return render(request, 'users/dashboard.html', {})

    def post(self, request, *args, **kwargs):


        bot = InstaBot(
            login=take_cred().insta_user,
            password=take_cred().insta_pass,
            like_per_day=1000,
            comments_per_day=0,
            #aqui tengo que usar la funcion que me devuelve el query set para asignarle los hastgs en un for de el queryset que me esta devolviendo
            tag_list=['misamigos'],
            tag_blacklist=['rain', 'thunderstorm'],
            user_blacklist={},
            max_like_for_one_tag=50,
            follow_per_day=300,
            follow_time=1 * 60,
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
                media = Media.objects.All().OrderBy('datetime')


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
                media = Media.objects.All().OrderBy('datetime')


            else:
                print("Wrong mode!")

        return render(request, 'dashboard.html', {})


