from django.db import models
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save


def upload_user_images(instance, filename):
    return f"users/{instance.user.username}/{filename}"


class Profile(models.Model):
    GOAL_CHOICES = (
        ('Business', 'business'),
        ('Client', 'client'),
    )
    profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to=upload_user_images, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    goal = models.CharField(max_length=100, choices=GOAL_CHOICES)

    def __str__(self):
        return self.profile.username


@receiver(post_save, sender=User)
def profile_post_save(instance, created, **kwargs):
    print(f"Signal received for User: {instance.username}")
    if created:
        profile = Profile(profile=instance)
        profile.save()
