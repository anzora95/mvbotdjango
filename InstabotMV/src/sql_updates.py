# -*- coding: utf-8 -*-
from django.db import connection
from django.db.models.query import QuerySet

from InstabotMV.models import Media, Username, Creds, HashtagList,Task
from datetime import datetime, time
from django.shortcuts import get_object_or_404
from InstabotMV.src.friendListscrap import validat


def check_and_update(self):

    pass


def check_already_liked(self, media_id): #media_ parametro cambiado el nombre a media_ins_id
        """ controls if media already liked before """

        # liked = get_object_or_404(Media, media_id=media_id)[:1]
        try:
            liked = Media.objects.get(media_id=media_id)
        except Media.DoesNotExist:
            liked = None

        if liked is not None:

            return 1
        else:
            return 0


def check_already_followed(self, user_id):
        """ controls if user already followed before """
        try:
            followed = Username.objects.get(username_id=user_id)
        except Username.DoesNotExist:
            followed = None

        if followed is not None:

            return 1

        else:
            return 0


def insert_media(self, media_id, status, code,owner_name, us, picUrl, task_id):#push funcional
    """ insert media to medias """
    now = datetime.now()
    med_insert = Media(
        media_id=media_id,
        status=status,
        datetime=str(now),
        code=code,
        owner_name=owner_name,
        cred_us=us,
        picUrl=picUrl,
        task_id=task_id

    )

    med_insert.save()


def insert_username(self, username_id, username, unfollow, us, picUrl, task_id):
    """ insert user_id to usernames """
    now = datetime.now()

    user_insert = Username(

        username=username,
        username_id=username_id,
        unfollow_count=unfollow,
        last_followed_time=str(now),
        cred_us=us,
        picUrl=picUrl,
        task_id=task_id

    )

    user_insert.save()


def insert_unfollow_count(use_nam,user_id=False, user=False):
    """ track unfollow count for new futures """

    if user_id:
        try:
            us = Username.objects.get(username_id=user_id, cred_us=use_nam)
        #print(str(us.username))
            us.unfollow_count = us.unfollow_count+1
            us.save()
        except:
            print('No se pudo hay registro repetido')    
    elif user:
        use = Username.objects.get(username=user)
        use.unfollow_count = use.unfollow_count+1
        use.save()
    else:
        return False

def update_creds(us_actual,new_pass=False,new_name=False):
    try:
        cr = Creds.objects.get(insta_user=us_actual)
        credito=1
    except:
        credito=0
        print('El usuario no ha podido ser encontrado')
    if credito==1:
        if new_pass and new_name:
            valid=validat(new_name,new_pass)
            if valid==2:
                cr.insta_user=new_name
                cr.insta_pass=new_pass
                cr.save()
                return 1#valor de retorno bandera para el mensaje
            else:
                print("El usuario y/o contraseña no son validos")
                return 2 #El usuario y/o contraseña no son validos
        elif new_pass:
            valid=validat(us_actual,new_pass)
            if valid==2:
                cr.insta_pass=new_pass
                cr.save()
                return 1#valor de retorno bandera para el mensaje
            else:
                print("La contraseña no es valida")
                return 3 #La contraseña no es valida
        elif new_name:
            pasw=cr.insta_pass
            valid=validat(new_name,pasw)
            if valid==2:
                cr.insta_user=new_name
                cr.save()
                return 1#valor de retorno bandera para el mensaje
            else:
                print("el usuario es incorrecto")
                return 4 #el usuario es incorrecto
    else:
        print("El usuario actual no es el correcto")
        return 5 #El usuario no ha podido ser encontrado


def sleep_mod(id_task):
    t= Task.objects.get(id=id_task)
    t.sleep_mod=1
    t.save()

def sleep_mod_off(id_task):
    t= Task.objects.get(id=id_task)
    t.sleep_mod=0
    t.save()

def get_usernames_first(self):
    """ Gets first element of usernames table """
    try:
        username = Username.objects.all[:5]
    except Username.DoesNotExist:
        username = None

    if username:
        return username
    else:
        return False


def get_usernames(self):
    """ Gets usernames table """
    try:
        usernames = Username.objects.all()
    except Username.DoesNotExist:
        usernames = None

    if usernames:
        return usernames
    else:
        return False


def get_username_random(self):
    """ Gets random username """
    try:
        username = Username.objects.filter(unfollow_count=0).order_by('?')[:1]
    except Username.DoesNotExist:
        username = None

    if username:
        return username
    else:
        return False


def check_and_insert_user_agent(self, user_agent):
    """ Verificando el User Agent en la base de datos  """

    # result_check = self.follows_db_c.execute("SELECT `settings_val` from settings where settings_name = 'USERAGENT'")
    # if result_check:
    #     result_get = result_check[0]
    #     return result_get
    # else:
    #     qry_insert = """
    #                 INSERT INTO settings (settings_name, settings_val)
    #                 VALUES ('USERAGENT', '%s')
    #                  """ % user_agent
    #     self.follows_db_c.execute(qry_insert)
    #     return check_and_insert_user_agent(self, user_agent)
    #
    # med_insert = self.Media(
    #
    #     media_id=media_ins,
    #     status=stat,
    #     datatime=str(now)
    # )
    # med_insert.save()

    # result_chek = Settings.objects.raw("select `settings_val` from instabotmv_settings where "
    #                                    "settings_name = 'USERAGENT'")
    # if result_chek:
    #     result_get = result_chek[0]
    #     return result_get
    # else:
    #     with connection.cursor() as cursor:
    #         cursor.execute("INSERT INTO instabotmv_settings (settings_name, settings_val) "
    #                        "VALUES ('USERAGENT', '%s')" % user_agent)
    #
    #         row = cursor.fetchone()
    #
    #     return check_and_insert_user_agent(row)
    pass


def take_cred():

    creds = Creds.objects.get()

    return creds


def insert_tag(self, catalogo, hashtags_names):

    hash_insert = HashtagList(
        catalogo=catalogo,
        hashtag_names=hashtags_names,
    )

    hash_insert.save()

# def get_id_creds(us):
#
#     user=Creds.object.filter(instauser=us)
#     id=
#
#
#     return

def count_ngage(task_id):
    us=Username.objects.filter(unfollow_count=0, task_id=task_id)

    return len(us)

def followed_ngage(usr_id):

    try:
        username=Username.objects.get(username_id=usr_id)
    except Username.DoesNotExist:
        username = None

    if username:
        insert_unfollow_count(usr_id)
    else:
        print("Usuario no seguido por ngage")
