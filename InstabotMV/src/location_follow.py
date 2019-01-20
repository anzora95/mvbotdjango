#FUNCION ISNTASWELL

url_location = 'https://www.instagram.com/explore/locations/%s/?__a=1'

def get_us_id_by_location(self, tag):  #seguir a un usuario por medio de un post con una ubicacion como la seleccionada 

    if tag.startswith('l:'):     #si en la lista de tags el tag empieza por una l: entra al if como una locacion
            tag = tag.replace('l:', '')
            self.by_location = True
            try:                
                r = self.s.get(url_location)
                data_location = json.loads(r.text)
                user_name = data_location['location']['edge_location_to_top_post']['edges']['0']['node']['owner']
                return user_name
            except:
                #write_log("Locations is wrong")
                return "No sew pudo completar la accion"
    else:
        return("This in not a location")
