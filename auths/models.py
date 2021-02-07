from django.db import models
from django.contrib.auth.models import User

from PIL import Image
import os

def user_directory_path(instance, filename):
    return 'profile_pics'

def user_directory_path2(instance, filename):
    return 'profile_pics'

def images_dir(file=""):
    if file != "":
        return os.path.join(os.path.abspath(os.path.dirname('media/images/')), file)
    else:
        return os.path.abspath(os.path.dirname('media/images/'))

def user_path(instance, filename):
    from os.path import basename
    basename(filename)
    filename, fileExtension = os.path.splitext(filename)
    return '{}/{}/{}{}'.format('profile_pics', instance.user.id, hash(filename), fileExtension)

def user_path_thumb(instance, filename):
    from os.path import basename
    basename(filename)
    filename, fileExtension = os.path.splitext(filename)
    return '{}/{}/{}/{}{}{}'.format('profile_pics', instance.user.id, 'thumb', hash(filename), '_thumb', fileExtension)

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=user_path, null=True, blank=True, default="images/DefaultUserIcon.png")
    profile_pic_thumb = models.ImageField(upload_to=user_path_thumb, null=True, blank=True, default="images/DefaultUserIcon.png")
    biography = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=30, null=True, blank=True)
    is_creator = models.BooleanField(default=False, help_text="Designates that this user is in creator's team")
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_pic.path)
        img_thumb = Image.open(self.profile_pic_thumb.path)
        
        if img.height > 300 or  img.width > 300:
            img = img.resize((300, 300), Image.ANTIALIAS) #Image.NEAREST, Image.LANCZOS, Image.BILINEAR, Image.BICUBIC, Image.BOX, Image.HAMMING
            img.save(self.profile_pic.path, quality=100)
         
        img_thumb = img_thumb.resize((50, 50), Image.ANTIALIAS)
        img_thumb.save(self.profile_pic_thumb.path, quality=100)

  
    def delete(self, *args, **kwargs):
        storage1, path1 = self.profile_pic.storage, self.profile_pic.path
        storage2, path2 = self.profile_pic_thumb.storage, self.profile_pic_thumb.path
        if path1 != images_dir("DefaultUserIcon.png") and path2 != images_dir("DefaultUserIcon.png"):
            storage1.delete(path1)
            storage2.delete(path2)
        else:
            pass
  
    def __str__(self):
        return self.user.username

 
