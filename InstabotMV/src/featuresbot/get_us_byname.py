import json
import logging


def get_username_by_user_id(self, user_id):
    """ Get username by user_id """
    if self.login_status:
        try:
            url_info = self.api_user_detail % user_id
            r = self.s.get(url_info, headers="")
            all_data = json.loads(r.text)
            username = all_data["user"]["username"]
            return username
        except:
            logging.exception("Except on get_username_by_user_id")
            return False
    else:
        return False