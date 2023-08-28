from django.db import models
from shoes.models import Shoe
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

class Auction(models.Model):
    title = models.CharField(max_length=200)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name='auctions')
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_ended = models.BooleanField(default=False)
    ethereum_tx = models.CharField(max_length=100, blank=True, null=True)
    is_cache_cleared = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def is_expired(self):
        return self.end_date <= timezone.now()
    

    

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
