from datetime import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length= 255)
    description = models.TextField(null= True, blank= True)

    completed = models.BooleanField(default= False)

    # status_complete = models.TextChoices("Not Yet", "Started", "Finished")
    # completed = models.CharField(blank= True, choices= status_complete.choices)

    created_at = models.DateTimeField(auto_now_add= True)
    # start_at = models.DateTimeField(default= timezone.now)
    # finish_at = models.DateTimeField(null = True, blank= True)
    user = models.ForeignKey(User, on_delete= models.CASCADE, null= True, blank= True )

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['completed']