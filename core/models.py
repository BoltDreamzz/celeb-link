from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Celebrity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Optional: can login
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='celebrity/profile_pics/')
    hero_image = models.ImageField(upload_to='celebrity/hero_images/', blank=True, null=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    merch_link = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    followers = models.TextField(blank=True, default="2.8")  # Optional: can be updated by the user
    projects = models.TextField(blank=True, default="78")  # Optional: can be updated by the user
    awards = models.TextField(blank=True, default="8")  # Optional: can be updated by the user
    years_active = models.TextField(blank=True, default="5")  # Optional: can be updated by the user

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Media(models.Model):
    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE, related_name='media')
    MEDIA_TYPES = [
        ('photo', 'Photo'),
        ('video', 'Video')
    ]
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    url = models.URLField()
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.media_type} for {self.celebrity.name}"


class MembershipTier(models.Model):
    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE, related_name='tiers')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.celebrity.name}"


class Fan(models.Model):
    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE, related_name='fans')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    membership_tier = models.ForeignKey(MembershipTier, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - Fan of {self.celebrity.name}"


class Show(models.Model):
    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE, related_name='shows')
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    ticket_link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.celebrity.name}"