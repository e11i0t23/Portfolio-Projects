from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from .models import User, Auction, AuctionForm, Bid, BidForm, Comment, CommentForm

from datetime import datetime, timezone



def index(request):
    auctions = Auction.objects.all().filter(endDate__gte=datetime.now(timezone.utc))
    if 'category' in request.GET:
        currentCategory = request.GET['category']
        print(currentCategory)
        if 'ALL' not in currentCategory:
            auctions = auctions.filter(category=currentCategory)
    
    for auction in auctions:
        maxbid = auction.placed_bids.aggregate(Max('bid'))['bid__max']
        auction.max_bid = maxbid if maxbid is not None else auction.startingBid

    return render(request, "project_2_commerce/index.html", {
        "auctions": auctions,
        "categories": Auction.categories
    })

@login_required(login_url='/login')
def watching(request):    
    auctions = Auction.objects.all().filter(watchers=request.user)
    for auction in auctions:
        maxbid = auction.placed_bids.aggregate(Max('bid'))['bid__max']
        auction.max_bid = maxbid if maxbid is not None else auction.startingBid
    return render(request, "project_2_commerce/index.html", {
        "auctions": auctions,
        "watching": True
    })

@login_required(login_url='/login')
def edit(request):
    if request.method == "POST":
        a = Auction(user=request.user)
        f = AuctionForm(request.POST, instance=a)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect(reverse("project_2_commerce/index"))
        else:
            return render(request, "project_2_commerce/edit.html", {
                "form": f
            })

    return render(request, "project_2_commerce/edit.html", {
        "form": AuctionForm(data={"user":request.user})
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("project_2_commerce/index"))
        else:
            return render(request, "project_2_commerce/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "project_2_commerce/login.html")

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("project_2_commerce/index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "project_2_commerce//register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "project_2_commerce/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("project_2_commerce/index"))
    else:
        return render(request, "project_2_commerce/register.html")
    

def auctionpage(request, auc):
    auction = Auction.objects.get(pk=auc)
    auction.maxbid = auction.placed_bids.aggregate(Max('bid'))['bid__max']
    if auction.maxbid == None: auction.maxbid = auction.startingBid
    cf = CommentForm()
    bf = BidForm(data={"bid":auction.maxbid+1 })

    if 'e' in request.GET and request.user == auction.user:
        auction.endDate = datetime.now()
        auction.save()
        return HttpResponseRedirect(reverse("project_2_commerce/auctionpage", args=(auction.id,)))
    elif 'w' in request.GET:
        if request.user in auction.watchers.all():
            auction.watchers.remove(request.user)
        else:
            auction.watchers.add(request.user)
        auction.save()
        return HttpResponseRedirect(reverse("project_2_commerce/auctionpage", args=(auction.id,)))

    if request.method == "POST":
        if 'comment' in request.POST:
            c = Comment(user=request.user, auction=auction)
            cf = CommentForm(request.POST, instance=c)
            if cf.is_valid():
                cf.save()
                return HttpResponseRedirect(reverse("project_2_commerce/auctionpage", args=(auction.id,)))


        elif 'bid' in request.POST:
            b = Bid(user=request.user, auction=auction)
            bf = BidForm(request.POST, instance=b)
            if bf.is_valid():
                maxbid = auction.placed_bids.aggregate(Max('bid'))['bid__max']
                if maxbid is None: maxbid = auction.startingBid
                if bf.cleaned_data['bid'] > maxbid:
                    bf.save()
                    return HttpResponseRedirect(reverse("project_2_commerce/auctionpage", args=(auction.id,)))
                else:
                    bf.add_error('bid', 'Bid is too low')

    active = (True if datetime.now(auction.endDate.tzinfo) < auction.endDate else False)
    
    if datetime.now(auction.endDate.tzinfo) >= auction.endDate:
        if auction.maxbid is not None:
            auction.winner = Bid.objects.get(auction=auction, bid=auction.maxbid).user
        else:
            auction.winner = auction.user

    return render(request, "project_2_commerce/auctionpage.html",{
        "auction": auction,
        "bidForm": bf,
        "commentForm": cf,
        "comments": Comment.objects.all().filter(auction=auction),
        "watching": "UnWatch" if request.user in auction.watchers.all() else "Watch"
    })
