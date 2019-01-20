import logging
from InstabotMV.src.sql_updates import insert_username


def follow(self, user_id):
    """ Send http request to follow """
    if self.login_status:
        url_follow = self.url_follow % (user_id)
        try:
            follow = self.s.post(url_follow)
            if follow.status_code == 200:
                self.follow_counter += 1
                log_string = "Followed: %s #%i." % (user_id,
                                                    self.follow_counter)
                self.write_log(log_string)
                username = self.get_username_by_user_id(user_id=user_id)
                insert_username(self, user_id=user_id, username=username)
            return follow
        except:
            logging.exception("Except on follow!")
    return False