from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    bio = models.TextField(max_length=150, verbose_name='Bio', null=True)
    profile_image = CloudinaryField('profile_image')
    email_confirmed = models.BooleanField(default=False, verbose_name='Is Confirmed?')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date Updated')

    def get_followers(self): # people who follow the user
        return self.followers.all()

    def get_following(self): # people who the user follow
        return self.following.all()
    
    def __str__(self):
        return str(self.user)
    
    class Meta:
        verbose_name_plural = 'Profiles'