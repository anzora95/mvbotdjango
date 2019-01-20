import random
import datetime
import time
from InstabotMV.src.sql_updates import check_already_liked
from InstabotMV.src.sql_updates import check_already_followed
from InstabotMV.src.unfollow_protocol import unfollow_protocol
from InstabotMV.src.location_follow import get_us_id_by_location

def auto_mod(self):
    """ Star loop, that get media ID by your tag list, and like it """
    if self.login_status:
        while True:
            random.shuffle(self.tag_list)
            self.get_media_id_by_tag(random.choice(self.tag_list))
            self.like_all_exist_media(random.randint \
                                          (1, self.max_like_for_one_tag))


def new_auto_mod(self):
    while True:
        now = datetime.datetime.now()
        if (
                datetime.time(self.start_at_h, self.start_at_m) <= now.time()
                and now.time() <= datetime.time(self.end_at_h, self.end_at_m)
        ):
            # ------------------- Get media_id -------------------
            if len(self.media_by_tag) == 0:
                self.get_media_id_by_tag(random.choice(self.tag_list))
                self.this_tag_like_count = 0
                self.max_tag_like_count = random.randint(
                    1, self.max_like_for_one_tag)
                self.remove_already_liked()
            # ------------------- Like -------------------
            self.new_auto_mod_like()
            # ------------------- Follow -------------------
            self.mod_follow_by_locations()
            # ------------------- Unfollow -------------------
            self.mod_follow_by_locations()
            # ------------------- Comment -------------------
            # self.new_auto_mod_comments()
            # Bot iteration in 1 sec
            time.sleep(3)
            # print("Tic!")
        else:
            print("sleeping until {hour}:{min}".format(hour=self.start_at_h,
                                                       min=self.start_at_m), end="\r")
            time.sleep(100)


def remove_already_liked(self):
    self.write_log("Removing already liked medias..")
    x = 0
    while x < len(self.media_by_tag):
        if check_already_liked(self, media_id=self.media_by_tag[x]['node']['id']) == 1:
            self.media_by_tag.remove(self.media_by_tag[x])
        else:
            x += 1


def new_auto_mod_like(self):
    if time.time() > self.next_iteration["Like"] and self.like_per_day != 0 \
            and len(self.media_by_tag) > 0:
        # You have media_id to like:
        if self.like_all_exist_media(media_size=1, delay=False):
            # If like go to sleep:
            self.next_iteration["Like"] = time.time() + \
                                          self.add_time(self.like_delay)
            # Count this tag likes:
            self.this_tag_like_count += 1
            if self.this_tag_like_count >= self.max_tag_like_count:
                self.media_by_tag = [0]
        # Del first media_id
        del self.media_by_tag[0]


def new_auto_mod_follow(self):  # da follow en base a la media que tiene en media_by_tag
    if time.time() > self.next_iteration["Follow"] and \
            self.follow_per_day != 0 and len(self.media_by_tag) > 0:
        if self.media_by_tag[0]['node']["owner"][
            "id"] == self.user_id:  # Esta parte de la funcion la ocupa para no autolikearse
            self.write_log("Keep calm - It's your own profile ;)")
            return
        if check_already_followed(self, user_id=self.media_by_tag[0]['node']["owner"]["id"]) == 1:
            self.write_log("Already followed before " + self.media_by_tag[0]['node']["owner"][
                "id"])  # aqui se cuestiona si el usuario ya fue followed para no darle follow de nuevo
            self.next_iteration["Follow"] = time.time() + \
                                            self.add_time(self.follow_delay / 2)
            return
        log_string = "Trying to follow: %s" % (
            self.media_by_tag[0]['node']["owner"]["id"])
        self.write_log(log_string)

        if self.follow(self.media_by_tag[0]['node']["owner"]["id"]) != False:
            self.bot_follow_list.append(
                [self.media_by_tag[0]['node']["owner"]["id"],
                 time.time()])  # en este if se agrega a la lista de usuarios ya seguidos en bot_follow_list
            self.next_iteration["Follow"] = time.time() + \
                                            self.add_time(self.follow_delay)  # aqui espera la siguiente iteracion


def mod_follow_by_locations(self):
    if time.time() > self.next_iteration["Follow"] and \
            self.follow_per_day != 0 and len(self.media_by_tag) > 0:
        # if self.media_by_tag[0]['node']["owner"]["id"] == self.user_id:  #Esta parte de la funcion la ocupa para no autolikearse
        #   self.write_log("Keep calm - It's your own profile ;)")
        user_prov_id = get_us_id_by_location(self, "l:111948542155151")

        if user_prov_id == self.user_id:
            self.write_log(
                "Its your own profile")  # Esta parte de la funcion la ocupa para no autoagregarse lño cual es imposible pero daria un error en ejecucion

            return
            if check_already_followed(self, user_id=user_prov_id) == 1:
                self.write_log(
                    "Already followed before " + user_prov_id)  # aqui se cuestiona si el usuario ya fue followedpara no darle follow de nuevo
                self.next_iteration["Follow"] = time.time() + \
                                                self.add_time(self.follow_delay / 2)
                return
                log_string = "Trying to follow: %s" % (user_prov_id)
                self.write_log(log_string)

                if self.follow(user_prov_id) != False:
                    self.bot_follow_list.append(
                        [user_prov_id,
                         time.time()])  # en este if se agrega a la lista de usuarios ya seguidos en bot_follow_list
                    self.next_iteration["Follow"] = time.time() + \
                                                    self.add_time(
                                                        self.follow_delay)  # aqui espera la siguiente iteracion


def new_auto_mod_unfollow(self):
    if time.time() > self.next_iteration["Unfollow"] and self.unfollow_per_day != 0:
        if self.bot_mode == 0:
            log_string = "Trying to unfollow #%i: " % (self.unfollow_counter + 1)
            self.write_log(log_string)
            self.auto_unfollow()
            self.next_iteration["Unfollow"] = time.time() + \
                                              self.add_time(self.unfollow_delay)
        if self.bot_mode == 1:
            unfollow_protocol(self)


def new_auto_mod_comments(self):
    if time.time() > self.next_iteration["Comments"] and self.comments_per_day != 0 \
            and len(self.media_by_tag) > 0 \
            and self.check_exisiting_comment(self.media_by_tag[0]['node']['shortcode']) == False:
        comment_text = self.generate_comment()
        log_string = "Trying to comment: %s" % (self.media_by_tag[0]['node']['id'])
        self.write_log(log_string)
        if self.comment(self.media_by_tag[0]['node']['id'], comment_text) != False:
            self.next_iteration["Comments"] = time.time() + \
                                              self.add_time(self.comments_delay)