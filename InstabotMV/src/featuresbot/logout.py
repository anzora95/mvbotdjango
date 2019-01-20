import datetime
import logging



def logout(self):
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