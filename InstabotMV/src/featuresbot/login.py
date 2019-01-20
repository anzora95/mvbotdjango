import time
import random
from InstabotMV.src.userinfo import UserInfo

def login(self):
    log_string = 'Trying to login as %s...\n' % (self.user_login)
    self.write_log(log_string)
    self.login_post = {
        'username': self.user_login,
        'password': self.user_password
    }

    self.s.headers.update({
        'Accept': '*/*',
        'Accept-Language': self.accept_language,
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Host': 'www.instagram.com',
        'Origin': 'https://www.instagram.com',
        'Referer': 'https://www.instagram.com/',
        'User-Agent': self.user_agent,
        'X-Instagram-AJAX': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest'
    })

    r = self.s.get(self.url)
    self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
    time.sleep(5 * random.random())
    login = self.s.post(
        self.url_login, data=self.login_post, allow_redirects=True)
    self.s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
    self.csrftoken = login.cookies['csrftoken']
    # ig_vw=1536; ig_pr=1.25; ig_vh=772;  ig_or=landscape-primary;
    self.s.cookies['ig_vw'] = '1536'
    self.s.cookies['ig_pr'] = '1.25'
    self.s.cookies['ig_vh'] = '772'
    self.s.cookies['ig_or'] = 'landscape-primary'
    time.sleep(5 * random.random())

    if login.status_code == 200:
        r = self.s.get('https://www.instagram.com/')
        finder = r.text.find(self.user_login)
        if finder != -1:
            ui = UserInfo()
            self.user_id = ui.get_user_id_by_login(self.user_login)
            self.login_status = True
            log_string = '%s login success!' % (self.user_login)
            log_extra = '%i this a tag' % (self.bot_mode)
            self.write_log(log_string)
        else:
            self.login_status = False
            self.write_log('Login error! Check your login data!')
    else:
        self.write_log('Login error! Connection error!')
