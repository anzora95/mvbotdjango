import json
import logging


def get_media_id_by_tag(self, tag):
    """ Get media ID set, by your hashtag or location """

    if self.login_status:
        if tag.startswith('l:'):  # si en la lista de tags el tag empieza por una l: entra al if como una locacion
            tag = tag.replace('l:', '')
            self.by_location = True
            log_string = "Get Media by location: %s" % (tag)
            self.write_log(log_string)
            if self.login_status == 1:
                url_location = self.url_location % (tag)
                try:
                    r = self.s.get(url_location)
                    all_data = json.loads(r.text)
                    self.media_by_tag = list(all_data['graphql']['location']['edge_location_to_media']['edges'])
                except:
                    self.media_by_tag = []
                    self.write_log("Except on get_media!")
                    logging.exception("get_media_id_by_tag")
            else:
                return 0

        else:
            log_string = "Get Media by tag: %s" % (tag)  # sino ignora el if de arriba y comienza a buscar por tag
            self.by_location = False
            self.write_log(log_string)
            if self.login_status == 1:
                url_tag = self.url_tag % \
                    (tag)  # combina la url de busqueda de tags con el nombre del tag asignado para la busqueda
                try:
                    r = self.s.get(url_tag)  # busca obtener un objeto json de la busqueda
                    all_data = json.loads(r.text)  # si lo hace carga el json y lo transforma en texto
                    self.media_by_tag = list(all_data['graphql']['hashtag']['edge_hashtag_to_media']['edges'])
                except:
                    self.media_by_tag = []
                    self.write_log("Except on get_media!")
                    logging.exception("get_media_id_by_tag")
            else:
                return 0
