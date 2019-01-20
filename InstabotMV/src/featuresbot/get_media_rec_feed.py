import datetime
import json
import logging
import time


def get_media_id_recent_feed(self):
    if self.login_status:
        now_time = datetime.datetime.now()
        log_string = "%s : Get media id on recent feed" % (self.user_login)
        self.write_log(log_string)
        if self.login_status == 1:
            url_tag = 'https://www.instagram.com/?__a=1'
            try:
                r = self.s.get(url_tag)
                all_data = json.loads(r.text)

                self.media_on_feed = list(
                    all_data['graphql']['user']['edge_web_feed_timeline'][
                        'edges'])

                log_string = "Media in recent feed = %i" % (
                    len(self.media_on_feed))
                self.write_log(log_string)
            except:
                logging.exception("get_media_id_recent_feed")
                self.media_on_feed = []
                time.sleep(20)
                return 0
        else:
            return 0