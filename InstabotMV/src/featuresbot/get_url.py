def get_instagram_url_from_media_id(self, media_id, url_flag=True,
                                    only_code=None):  # obtiene una url completa con el media_id
    """ Get Media Code or Full Url from Media ID Thanks to Nikished """
    media_id = int(media_id)
    if url_flag is False:
        return ""
    else:
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
        shortened_id = ''
        while media_id > 0:
            media_id, idx = divmod(media_id, 64)
            shortened_id = alphabet[idx] + shortened_id
        if only_code:
            return shortened_id
        else:
            return 'instagram.com/p/' + shortened_id + '/'