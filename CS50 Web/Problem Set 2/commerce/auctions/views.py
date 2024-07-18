from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Enter your comment here'}),
        }

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(closed=False)
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


def listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    
    highest_bid = listing.bids.order_by('-amt').first()
    highest_bid = highest_bid.amt if highest_bid else listing.starting_bid
    
    is_in_watchlist = False
    if request.user.is_authenticated:
        is_in_watchlist = Watchlist.objects.filter(user=request.user, listing_id=listing).exists()
    
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.listing_id = listing
            new_comment.user = request.user
            new_comment.save()
            return redirect('listing', listing_id=listing_id)
    else:
        comment_form = CommentForm()

    comments = listing.comments.order_by('-time')
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_in_watchlist": is_in_watchlist,
        "highest_bid": highest_bid,
        "comment_form": comment_form,
        "comments": comments
     })


@login_required
def watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    is_in_watchlist = Watchlist.objects.filter(user=user, listing_id=listing).exists()
    
    if request.method == "POST":
        if not is_in_watchlist:
            Watchlist.objects.create(user=user, listing_id=listing)
        else:
            Watchlist.objects.filter(user=user, listing_id=listing).delete()

    return redirect('listing', listing_id=listing_id)


@login_required
def bid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user

    if listing.closed:
        messages.error(request, "The auction is closed. No more bids are accepted.")
        return redirect('listing', listing_id=listing_id)
    
    if request.method == "POST":
        amt = request.POST.get("amt")
        if not amt:
            messages.error(request, "Bid amount is required.")
            return redirect('listing', listing_id=listing_id)
        
        amt = float(amt)
        highest_bid = listing.bid.aggregate(Max('amt'))['amt__max']

        if highest_bid is None:
            highest_bid = listing.starting_bid
        
        if amt <= highest_bid:
            messages.error(request, "Your bid must be higher than the current highest bid.")
            return redirect('listing', listing_id=listing_id)
        
        bid = Bid.objects.create(user=user, listing_id=listing, amt=amt)
        bid.save()
        messages.success(request, "Your bid has been placed successfully!")
        return redirect('listing', listing_id=listing_id)

    return redirect('listing', listing_id=listing_id)


@login_required
def close_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    if listing.closed:
        messages.info(request, "The auction is already closed.")
    else:
        if request.method == "POST":
            highest_bid = listing.bids.order_by('-amt').first()
        
            if highest_bid:
                listing.closed = True
                listing.winning_bid = highest_bid.amt
                listing.winning_user = highest_bid.user
                listing.save()
                messages.success(request, "The auction has been closed.")
            else:
                messages.error(request, "No bids have been placed on this listing.")

        else:
            listing.closed = True
            listing.save()
            messages.success(request, "The auction has been successfully closed.")

    return redirect('listing', listing_id=listing_id)


@login_required
def watchlist_page(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    return render(request, 'auctions/watchlist.html', {'watchlist_items': watchlist_items})


def categories(request):
    categories = Listing.objects.values_list('category', flat=True).distinct()
    return render(request, 'auctions/categories.html', {'categories': categories})


def category_listings(request, category_name):
    listings = Listing.objects.filter(category=category_name, closed=False)
    return render(request, 'auctions/category_listings.html', {'listings': listings, 'category_name': category_name})
