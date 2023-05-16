from django.db import models
from users.models import NewUser
from django.urls import reverse
from PIL import Image

AppCategory = (
    ("EN","Entertainment"),
    ("SP","Sports")
)

SubCategory = (
    ("SM","Social Media"),
    ("MS", "Music"),
    ("EC", "Ecommerce")
)

class App(models.Model):
    app_name = models.CharField(max_length=300)
    app_link = models.CharField(max_length=500)
    points = models.IntegerField()
    app_image = models.ImageField(upload_to="app_images",blank=True,null=True)
    app_category = models.CharField(max_length = 2, choices=AppCategory)
    sub_category = models.CharField(max_length = 2, choices=SubCategory)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        if self.app_image:
            image=Image.open(self.app_image.path)
            if image.width > 500 or image.height > 500:
                output=(500,500)
                image.thumbnail(output)
                image.save(self.app_image.path)

    def __str__(self):
        return f"{self.app_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(NewUser,on_delete=models.CASCADE,related_name = "profile")
    profile_picture = models.ImageField(upload_to="profile_pics",default="defaultuser.png")


    def save(self,*args,**kwargs):
        if self.profile_picture:
            super().save(*args,**kwargs)
            image=Image.open(self.profile_picture.path)
            if image.width > 500 or image.height > 500:
                output=(500,500)
                image.thumbnail(output)
                image.save(self.profile_picture.path)
    
    def __str__(self):
        return f"{self.user.user_name}'s profile"

class Task(models.Model):
    app=models.ForeignKey(App,on_delete=models.CASCADE,related_name="apps")
    user=models.ForeignKey(NewUser,on_delete=models.CASCADE,related_name="appImages")
    image = models.ImageField(upload_to="user_app_images_uploads")
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.user_name}'s {self.app.app_name} image"