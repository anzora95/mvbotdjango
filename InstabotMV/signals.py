from django.db.models.signals import post_save
from InstabotMV import Media
from django.dispatch import receiver

@receiver(post_save, sender=Media)

def post_media_save(sender,instance,**kwargs):
	owner = Media.owner_name
	code = Media.code
	 print owner + code

