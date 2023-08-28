from django.db import models

class Shoe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    color = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
