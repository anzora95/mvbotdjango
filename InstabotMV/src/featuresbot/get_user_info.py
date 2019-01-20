import json
import logging


def get_userinfo_by_name(self, username):
    """ Get user info by name """

    if self.login_status:
        if self.login_status == 1:
            url_info = self.url_user_detail % (username)
            try:
                r = self.s.get(url_info)
                all_data = json.loads(r.text)
                user_info = all_data['user']
                follows = user_info['follows']['count']  # en la url del json ya no se llama follows sino edge_follows
                follower = user_info['followed_by'][
                    'count']  # en la url del json ya no se llama follows sino edge_followed_by
                follow_viewer = user_info['follows_viewer']
                if follower > 3000 or follows > 1500:
                    self.write_log('   >>>This is probably Selebgram, Business or Fake account')
                if follow_viewer:
                    return None
                return user_info  # aqui retorna el user info con todos los valores llenos si el usuario targeteado no sigue a nuestra cuenta
            except:
                logging.exception("Except on get_userinfo_by_name")
                return False
        else:
            return False