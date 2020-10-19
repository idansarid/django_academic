from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Bulletin(models.Model):
    body = models.TextField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.TextField()
    address = models.TextField()
    email = models.TextField()


class Sender(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Receiver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Message(models.Model):
    sender = models.ForeignKey(Sender, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Receiver, on_delete=models.CASCADE)
    message = models.TextField()
    subject = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


