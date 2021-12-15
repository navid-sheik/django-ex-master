from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.urls import reverse_lazy
from PIL import Image
import json

# Create your models here.





class User(AbstractUser):
    username  = models.CharField(max_length=50, unique=True)
    #hobbies  =  models.ManyToManyField("Hobby", blank=True)

    friends = models.ManyToManyField(
        to='self',
        blank=True,
       
        symmetrical=True,
        
    )

    def to_dict(self):
        return{
            'id' : self.id,
            'username': self.username,
            'email' : self.email,
            'hobbies': [hobby.to_dict() for hobby in self.hobby_set.all()],
            'friends': [friend.id for friend in self.friends.all()],
            'profile' :  self.profile.to_dict(),
            'api' : reverse_lazy("mainapp:send_friend_request", kwargs= {'to_user_id' : self.id})
        }
    
class Hobby (models.Model):
    name = models.CharField(max_length=50)
    users  =  models.ManyToManyField(User, blank=True)

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'users': [user.username for user in self.users.all()],
            'api' :  reverse_lazy("mainapp:delete_hobby",kwargs= {'hobby_id' : self.id})
        }
    def __str__(self) -> str:
        return self.name
# class User_Hobby(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     hobby  = models.ForeignKey(Hobby, on_delete=models.CASCADE)


class FriendRequest(models.Model):

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="request_sent",
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="request_received",
    )

    def to_dict(self):
        return{
            'from_user': self.from_user.to_dict(),
            'to_user':self.to_user.to_dict(),
        }


    def __str__(self) -> str:
        return self.to_user.username





class Profile(models.Model):
    image =  models.ImageField(default='default_profile.png', upload_to='profile_images')
    city  =  models.CharField(max_length=200, null=True)
    dob  =  models.DateField("dob", null=True)
    user  =  models.OneToOneField(User, null=True, on_delete=models.CASCADE)


    def to_dict(self):
        return{
            'profile_image': self.image.url,
            'city' :  self.city,
            'dob' :  self.dob,
  
            
            
        }


    

    



    


