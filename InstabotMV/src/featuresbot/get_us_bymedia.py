import json
import logging



def get_username_by_media_id(self, media_id):
    """ Get username by media ID Thanks to Nikished """

    if self.login_status:
        if self.login_status == 1:
            media_id_url = self.get_instagram_url_from_media_id(int(media_id), only_code=True)
            url_media = self.url_media_detail % (media_id_url)
            try:
                r = self.s.get(url_media)
                all_data = json.loads(r.text)

                username = str(all_data['graphql']['shortcode_media']['owner']['username'])
                self.write_log("media_id=" + media_id + ", media_id_url=" +
                               media_id_url + ", username_by_media_id=" + username)
                return username
            except:
                logging.exception("username_by_mediaid exception")
                return False
        else:
            return ""