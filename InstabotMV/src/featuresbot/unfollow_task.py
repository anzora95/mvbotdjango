import logging
import time


def unfollow(self, user_id):
    """ Send http request to unfollow """
    if self.login_status:
        url_unfollow = self.url_unfollow % (user_id)
        try:
            unfollow = self.s.post(url_unfollow)
            if unfollow.status_code == 200:
                self.unfollow_counter += 1
                log_string = "Unfollowed: %s #%i." % (user_id,
                                                      self.unfollow_counter)
                self.write_log(log_string)
            return unfollow
        except:
            logging.exception("Exept on unfollow!")
    return False


def unfollow_on_cleanup(self, user_id):
    """ Unfollow on cleanup by @rjmayott """
    if self.login_status:
        url_unfollow = self.url_unfollow % (user_id)
        try:
            unfollow = self.s.post(url_unfollow)
            if unfollow.status_code == 200:
                self.unfollow_counter += 1
                log_string = "Unfollow: %s #%i of %i." % (
                    user_id, self.unfollow_counter, self.follow_counter)
                self.write_log(log_string)
            else:
                log_string = "Slow Down - Pausing for 5 minutes so we don't get banned!"
                self.write_log(log_string)
                time.sleep(300)
                unfollow = self.s.post(url_unfollow)
                if unfollow.status_code == 200:
                    self.unfollow_counter += 1
                    log_string = "Unfollow: %s #%i of %i." % (
                        user_id, self.unfollow_counter,
                        self.follow_counter)
                    self.write_log(log_string)
                else:
                    log_string = "Still no good :( Skipping and pausing for another 5 minutes"
                    self.write_log(log_string)
                    time.sleep(300)
                return False
            return unfollow
        except:
            log_string = "Except on unfollow... Looks like a network error"
            logging.exception(log_string)
    return False