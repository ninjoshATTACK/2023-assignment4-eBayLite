from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .forms import ListingForm, CommentForm, BidForm
from .models import User, Listing, Category, Comment, Watchlist, Bid

def getLastPk(obj):
    if(obj.objects.first() is None):
        return 1
    else:
        get_pk = obj.objects.order_by('-pk')[0]
        last_pk = get_pk.pk +1
        return last_pk

###############################Index Page#####################################
def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all()
    })

#############################Create Listings##################################
def create(request):
    if request.method == "POST":
        listing_form = ListingForm(request.POST, request.FILES)
        message = ""

        if listing_form.is_valid():
            new_listing = listing_form.save(commit=False)
            new_listing.seller = request.user
            new_listing.save()
            messages.success(request, (f'\"{ listing_form.cleaned_data["title"] }\" was successfully added!'))
            return redirect('listing', listing_id=new_listing.id)
        else:
            message = "Invalid form, try again."
            return render(request, "auctions/create.html", {
                "listing_form": listing_form,
                "message": message
            })

    else:
        listing_form = ListingForm()
        
        return render(request, "auctions/create.html", {
            "listing_form": listing_form, "categories": Category.objects.all()
        })

#############################Displays listings################################
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        'listing': listing, 'comment_form': CommentForm(), 'comment': comment
    })

def close(request, listing_id):
    listingtoclose = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.filter(listing=listingtoclose)
    final_price = bids.order_by('-price')[0]
    winner = User

    for bid in bids:
        if bid.price == final_price.price:
            winner = bid.buyer
            listingtoclose.winner = winner
            listingtoclose.available = False
            listingtoclose.save()
    
    return redirect('listing', listing_id=listing_id)

################################Comments######################################
def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    if request.method == "POST":
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.commenter = request.user
            new_comment.listing = listing
            new_comment.save()
            return redirect('listing', listing_id=listing_id)
        else:
            pass #for now
    else:
        comment_form = CommentForm()
    return render(request, "auctions/listing.html", {
        'comment_form': comment_form, 'listing': listing
    })

################################Categories#####################################
def categories(request):
    return render(request, "auctions/categories.html", {
        'categories': Category.objects.all()
    })

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(category = category, available=True)

    return render(request, "auctions/category.html", {
        'listings': listings, "category": category
    })

################################Watchlist######################################
def watchlist(request):
    watchlist = Watchlist.objects.get(user = request.user)

    return render(request, "auctions/watchlist.html", {
        'watchlist': watchlist.watched_listings.all()
    })

def watchlist_add(request, listing_id):
    if request.user.is_authenticated:
        if Watchlist.objects.filter(user = request.user).exists():
            watchlist = Watchlist.objects.get(user = request.user)
        else:
            watchlist = Watchlist(id = getLastPk(Watchlist), user=request.user)

        listing = Listing.objects.get(id=listing_id)
        watchlist.save()
        watchlist.watched_listings.add(listing)
        watchlist.save()

    return render(request, "auctions/watchlist.html", {
        'watchlist': watchlist.watched_listings.all()
    })

def watchlist_remove(request, listing_id):
    if request.user.is_authenticated:
        listing = Listing.objects.get(id=listing_id)
        watchlist = Watchlist.objects.get(user = request.user).watched_listings.remove(listing)

    return redirect('watchlist')

##################################Bidding######################################
def bid(request, listing_id):
    if request.user.is_authenticated:
        listing = Listing.objects.get(pk=listing_id)
        message = ""

        if request.method == "POST":
            bid_form = BidForm(request.POST, request.FILES)

            if bid_form.is_valid():
                new_bid = bid_form.save(commit=False)
                if new_bid.price > listing.startbid:
                    new_bid.buyer = request.user
                    new_bid.listing = listing
                    new_bid.save()
                    listing.startbid = new_bid.price
                    listing.save()
                    return redirect('listing', listing_id=listing_id)
                else:
                    message = "Something went wrong with the bid (your bid must be higher than current price)"
                    return render(request, "auctions/bid.html", {
                        "bid_form": bid_form, "message": message, "listing": listing
                    })
        else:
            bid_form = BidForm()
        
        return render(request, "auctions/bid.html", {
            "bid_form": bid_form, "listing": listing,
        })

        

#############################Login/Logout stuff################################
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
