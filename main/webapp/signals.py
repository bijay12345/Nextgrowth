from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from users.models import NewUser

@receiver(post_save,sender=NewUser)
def create_profile(sender,instance=None,created=False,**kwargs):
	if created:
		UserProfile.objects.create(user=instance)