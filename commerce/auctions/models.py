from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
    

    

class Product(models.Model):
    productName = models.CharField(max_length=128)
    productImage = models.URLField(default="https://cdn-icons-png.flaticon.com/512/7130/7130776.png")
    productOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", default = 1)
    productCategory = models.CharField(max_length=128, null=True, blank=True)
    productListed = models.BooleanField(default=True)
    productWinner = models.ForeignKey(User,on_delete=models.CASCADE, related_name="winner", null=True, blank=True)
    

    def __str__(self):
        return f"{self.productName} || {self.productOwner} || {self.productImage} || {self.productCategory} || {self.productListed} || {self.productWinner}"

class Bid(models.Model):
    bidPrice = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="productprice", null=True, blank=True)
    
    def __str__(self):
        
        return f"{self.bidPrice} || {self.bidder} {self.product} "

class Comments(models.Model):
    commentcontent = models.CharField(max_length=1000)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentid", default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)

    def __str__(self):
        return f"{self.commentcontent} || {self.commentator}"
    
class Watchlist(models.Model):
    watchlistShow = models.BooleanField(default=False)
    watchlistUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlistUser", null=True, blank=True)
    watchlistProduct = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="watchlistProduct", null=True, blank=True)
    
    def __str__(self):
        return f"{self.watchlistShow} || {self.watchlistUser} || {self.watchlistProduct}"
    

