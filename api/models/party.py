from django.db import models
from .user import User

# https://docs.djangoproject.com/en/5.1/topics/db/models/

class Party(models.Model):
    
    password = models.TextField()
    party_name = models.TextField()
    users = models.ManyToManyField(User)
    
    # Stringify
    def __str__(self):
        user_string = ""
        for user in self.users:
            user_string = user_string + "--" + str(user)
        return f"ui:{self.id} - party_name:{self.party_name} - users:{user_string}"