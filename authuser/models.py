from django.db import models
from django.contrib.auth.models import AbstractUser 

from shortuuid.django_fields import ShortUUIDField
import shortuuid
from django.db.models.signals import post_save


class User(AbstractUser):
    uid = ShortUUIDField(length=10, max_length=10, alphabet=shortuuid.get_alphabet())
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Profile(models.Model):
    uid = ShortUUIDField(length=10, max_length=10, alphabet=shortuuid.get_alphabet())
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image", default='avatar.png')
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200) # +234 (456) - 789
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}"


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

 
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)    



