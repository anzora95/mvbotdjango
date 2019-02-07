#necsito que busque en la base de datos un objeto con el id user que le voy a pasar sino lo encuentra que me devuelva un true para que pueda likear a ese usuario eso se podria lograr con un try catch

from InstabotMV.models import Media

us_repeted = False
def no_like_same_us(self,id_us):
     try:
         #Client.objects.filter(assigned_staff=request.user
         Media.objects.filter(owner_name=id_us)
     except:
        us_repeted=True

     return us_repeted

