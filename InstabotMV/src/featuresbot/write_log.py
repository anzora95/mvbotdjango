import datetime
import logging


def write_log(log_text, log_mod=0, log_file=0, log_file_path='', user_login='ajla'):

    """ Write log by print() or logger """
    if log_mod == 0:
        try:
            now_time = datetime.datetime.now()
            print(now_time.strftime("%d.%m.%Y_%H:%M") + " " + log_text)
        except UnicodeEncodeError:
            print("Your text has unicode problem!")
    elif log_mod == 1:
        # Create log_file if not exist.
        if log_file == 0:
            log_file = 1
            now_time = datetime.datetime.now()
            log_full_path = '%s%s_%s.log' % (
                log_file_path, user_login,
                now_time.strftime("%d.%m.%Y_%H:%M"))
            formatter = logging.Formatter('%(asctime)s - %(name)s '
                                          '- %(message)s')
            logger = logging.getLogger(user_login)
            hdrl = logging.FileHandler(log_full_path, mode='w')
            hdrl.setFormatter(formatter)
            logger.setLevel(level=logging.INFO)
            logger.addHandler(hdrl)
        # Log to log file.
        try:
            logger.info(log_text)
        except UnicodeEncodeError:
            print("Your text has unicode problem!")