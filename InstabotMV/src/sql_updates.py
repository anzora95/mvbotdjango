# -*- coding: utf-8 -*-
from django.db import connection
from django.db.models.query import QuerySet

from InstabotMV.models import Media, Username, Creds, HashtagList
from datetime import datetime, time
from django.shortcuts import get_object_or_404


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


def insert_media(self, media_id, status, code,owner_name, us):#push funcional
    """ insert media to medias """
    now = datetime.now()
    med_insert = Media(
        media_id=media_id,
        status=status,
        datetime=str(now),
        code=code,
        owner_name=owner_name,
        cred_us=us

    )

    med_insert.save()


def insert_username(self, username_id, username, unfollow, us):
    """ insert user_id to usernames """
    now = datetime.now()

    user_insert = Username(

        username=username,
        username_id=username_id,
        unfollow_count=unfollow,
        last_followed_time=str(now),
        cred_us=us
    )

    user_insert.save()


def insert_unfollow_count(self, user_id=False, user=False):
    """ track unfollow count for new futures """

    if user_id:
        us = Username.objects.get(username_id=user_id)
        us.unfollow_count = us.unfollow_count+1
        us.save()
    elif user:
        use = Username.objects.get(username=user)
        use.unfollow_count = use.unfollow_count+1
        use.save()
    else:
        return False


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
