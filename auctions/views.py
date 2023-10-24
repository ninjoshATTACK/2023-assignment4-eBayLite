from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .forms import ListingForm, CommentForm
from .models import User, Listing, Category, Comment, Watchlist

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
def watchlist(request, user):
    watchlist = Watchlist.objects.get() # I don't know how to pull the watchlist of the specific user

    return render(request, "auctions/watchlist.html", {
        'watchlist': watchlist
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
