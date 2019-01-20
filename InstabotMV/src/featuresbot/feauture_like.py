from InstabotMV.src.sql_updates import check_already_liked,insert_media
import sys
import logging
import time
import random


def like_all_exist_media(self, media_size=-1, delay=True):
    """ Like all media ID that have self.media_by_tag """

    if self.login_status:
        if self.media_by_tag != 0:
            i = 0
            for d in self.media_by_tag:
                # Media count by this tag.
                if media_size > 0 or media_size < 0:
                    media_size -= 1
                    l_c = self.media_by_tag[i]['node']['edge_liked_by']['count']
                    if ((l_c <= self.media_max_like and
                         l_c >= self.media_min_like) or
                            (self.media_max_like == 0 and
                             l_c >= self.media_min_like) or
                            (self.media_min_like == 0 and
                             l_c <= self.media_max_like) or
                            (self.media_min_like == 0 and
                             self.media_max_like == 0)):
                        for blacklisted_user_name, blacklisted_user_id in self.user_blacklist.items(
                        ):
                            if self.media_by_tag[i]['node']['owner'][
                                'id'] == blacklisted_user_id:
                                self.write_log(
                                    "Not liking media owned by blacklisted user: "
                                    + blacklisted_user_name)
                                return False
                        if self.media_by_tag[i]['node']['owner'][
                            'id'] == self.user_id:
                            self.write_log(
                                "Keep calm - It's your own media ;)")
                            return False
                        if check_already_liked(self, media_id=self.media_by_tag[i]['node']['id']) == 1:
                            self.write_log("Keep calm - It's already liked ;)")
                            return False
                        try:
                            if (len(self.media_by_tag[i]['node']['edge_media_to_caption']['edges']) > 1):
                                caption = self.media_by_tag[i]['node']['edge_media_to_caption'][
                                    'edges'][0]['node']['text'].encode(
                                    'ascii', errors='ignore')
                                tag_blacklist = set(self.tag_blacklist)
                                if sys.version_info[0] == 3:
                                    tags = {
                                        str.lower(
                                            (tag.decode('ASCII')).strip('#'))
                                        for tag in caption.split()
                                        if (tag.decode('ASCII')
                                            ).startswith("#")
                                    }
                                else:
                                    tags = {
                                        unicode.lower(
                                            (tag.decode('ASCII')).strip('#'))
                                        for tag in caption.split()
                                        if (tag.decode('ASCII')
                                            ).startswith("#")
                                    }

                                if tags.intersection(tag_blacklist):
                                    matching_tags = ', '.join(
                                        tags.intersection(tag_blacklist))
                                    self.write_log(
                                        "Not liking media with blacklisted tag(s): "
                                        + matching_tags)
                                    return False
                        except:
                            logging.exception("Except on like_all_exist_media")
                            return False

                        log_string = "Trying to like media: %s" % \
                                     (self.media_by_tag[i]['node']['id'])
                        self.write_log(log_string)
                        like = self.like(self.media_by_tag[i]['node']['id'])
                        # comment = self.comment(self.media_by_tag[i]['id'], 'Cool!')
                        # follow = self.follow(self.media_by_tag[i]["owner"]["id"])
                        if like != 0:
                            if like.status_code == 200:
                                # Like, all ok!
                                self.error_400 = 0
                                self.like_counter += 1
                                log_string = "Liked: %s. Like #%i." % \
                                             (self.media_by_tag[i]['node']['id'],
                                              self.like_counter)
                                insert_media(self,
                                             media_id=self.media_by_tag[i]['node']['id'],
                                             status="200", code=self.get_instagram_url_from_media_id(
                                        self.media_by_tag[i]['node']['id']), owner_name=self.get_username_by_media_id(
                                        self.media_by_tag[i]['node']['id']))
                                # log__string= "el url es  %s" %(url_media)
                                # log__string=get_instagram_url_from_media_id(self.media_by_tag[i]['node']['id'],True,None)   #se saca el url del media para poder ejecutarlo para asi ver el json para poder extraerel json del los datos del usuario
                                self.write_log(log_string)
                            elif like.status_code == 400:
                                log_string = "Not liked: %i" \
                                             % (like.status_code)
                                self.write_log(log_string)
                                insert_media(self,
                                             media_id=self.media_by_tag[i]['node']['id'],
                                             status="400")
                                # Some error. If repeated - can be ban!
                                if self.error_400 >= self.error_400_to_ban:
                                    # Look like you banned!
                                    time.sleep(self.ban_sleep_time)
                                else:
                                    self.error_400 += 1
                            else:
                                log_string = "Not liked: %i" \
                                             % (like.status_code)

                                insert_media(self,
                                             media_id=self.media_by_tag[i]['node']['id'],
                                             status=str(like.status_code))
                                log2extra = "Estado del bot %i" % (self.bot_mode)
                                self.write_log(log_string)
                                return False
                                # Some error.
                            i += 1
                            if delay:
                                time.sleep(self.like_delay * 0.9 +
                                           self.like_delay * 0.2 *
                                           random.random())
                            else:
                                return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
        else:
            self.write_log("No media to like!")


def like(self, media_id):
    """ Send http request to like media by ID """
    if self.login_status:
        url_likes = self.url_likes % (media_id)
        try:
            like = self.s.post(url_likes)
            last_liked_media_id = media_id
        except:
            logging.exception("Except on like!")
            like = 0
        return like


def unlike(self, media_id):
    """ Send http request to unlike media by ID """
    if self.login_status:
        url_unlike = self.url_unlike % (media_id)
        try:
            unlike = self.s.post(url_unlike)
        except:
            logging.exception("Except on unlike!")
            unlike = 0
        return unlike