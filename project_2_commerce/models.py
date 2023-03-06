from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, TextInput, Textarea, DateTimeInput, NumberInput, URLInput, Select
from datetime import datetime, timedelta, timezone


class Auction(models.Model):

    categories = [
        ('TECHNOLOGY', 'Electronics and Technology'),
        ('FASHION', 'Fashion'),
        ('COLLECTABLES', ' Arts and Collectables'),
        ('TOYS', 'Toys'),
        ('MEDIA', 'Books, Movies, and Music'),
        ('SPORTS', 'Sporting Goods'),
        ('HOME', 'Home and Furniture'),
        ('JEWLERY', 'Jewlery and Watches'),
        ('HEALTH', 'Health and Beauty'),
        ('DIY', 'Garden and DIY'),
        ('UNKNOWN', 'UNKNOWN'),
    ]

    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_auctions")
    startingBid = models.FloatField()
    description = models.TextField()
    image = models.URLField(blank=True)
    category = models.CharField(max_length=16, choices=categories, default='UNKNOWN')
    endDate = models.DateTimeField(default=(datetime.now(timezone.utc)+timedelta(days=7)))
    watchers = models.ManyToManyField(User, blank=True, related_name="watching")

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):

    bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="placed_bids")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} on {self.auction}: {self.bid}"


class Comment(models.Model):

    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_comments")

    def __str__(self):
        return f"{self.user} on {self.auction}: {self.comment}"
    

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        exclude = ['watchers', 'user']
        widgets= {
            'title': TextInput(attrs={'class':'form-control', 'required':'True'}),
            'category': Select(attrs={'class':"form-control"}),
            'startingBid': NumberInput(attrs={'class':"form-control"}),
            'endDate': DateTimeInput(attrs={'class':"form-control"}, format="%Y-%m-%d %H:%M"),
            'image': URLInput(attrs={'class':"form-control"}),
            'description': Textarea(attrs={'class':"form-control"}),
        }
        
    field_order = ['title', 'category', 'StartingBid', 'endDate', 'image', 'description']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        exclude = ['user', 'auction']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'auction']
        labels = {
           'comment' : '',
        }

