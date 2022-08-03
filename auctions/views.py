from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User,listing,bid,comment


def index(request):
    return render(request, "auctions/index.html",{
        "bidlist":listing.objects.filter(closed=False)
    })

categorieses=["books","electronics","vehicles","Mobile Phones","Home Appliances","Home and Furniture","Baby and Kids","Sports","Video Games","Movies & Tv Shows","Music","Fashion"]

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

@login_required(login_url='login')
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

@login_required(login_url='login')
def createlisting(request):
    if request.method == "POST":
        bids=listing()
        bids.title=request.POST["title"]
        bids.desc=request.POST["desc"]
        bids.img=request.POST["img"]
        bids.sbid=request.POST["stbid"]
        bids.seller=request.user
        bids.cbid=bids.sbid
        bids.categories=request.POST["cat"]
        bids.bidder=request.user
        bids.winner=bids.seller
        bids.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"auctions/createlisting.html",{
            "categories":categorieses
        })
    
def item(request,id):
    bids=listing.objects.get(id=id)
    if request.user==bids.seller:
        es=True
        fs=False
    elif request.user==bids.winner:
        es=False
        fs=True
    else:
        es=False
        fs=False
    return render(request,"auctions/items.html",{
        "bid":bids,
        "comments":comment.objects.filter(item=listing.objects.get(id=id)),
        "es":es,
        "fs":fs
    })

@login_required(login_url='login')
def comments(request,id):
    if request.method == "POST":
        com=comment()
        com.comment=request.POST["comment"]
        com.item=listing.objects.get(id=id)
        com.commenter=request.user
        com.save()
        return HttpResponseRedirect(reverse("item",args=(id,)))

@login_required(login_url='login')
def bidding(request,id):
    if request.method == "POST":
        bids=listing.objects.get(id=id)
        bidd=float(request.POST["bid"])
        if bidd>bids.cbid:
            bids.cbid=bidd
            bids.bidder=request.user
            bids.save()
            return HttpResponseRedirect(reverse("item",args=(id,)))
        else:
            return render(request,"auctions/items.html",{
                "bid":listing.objects.get(id=id),
                "comments":comment.objects.filter(item=listing.objects.get(id=id)),
                "message":"enter a higher bid!!"
            })

@login_required(login_url='login')
def bidclose(request,id):
    if request.method == "POST":
        bids=listing.objects.get(id=id)
        bids.closed=True
        bids.winner=bids.bidder
        bids.save()
        return HttpResponseRedirect(reverse("index"))

def category(request):
    if request.method == "GET":
        cate=request.GET.get("cate")
        return render(request,"auctions/categories.html",{
                "bidlist":listing.objects.all().filter(categories=cate),
                "categories":categorieses
            })
    else:
        return render(request,"auctions/categories.html",{
            "categories":categorieses
        })

@login_required(login_url='login')
def wonlist(request):
    return render(request,"auctions/wonlist.html",{
                    "bidlist":listing.objects.filter(closed=True,winner=request.user)
                })

@login_required(login_url='login')
def watches(request,id):
    if request.method == "POST":
        lists=listing.objects.get(id=id)
        lists.watcher=request.user
        lists.save()
        return HttpResponseRedirect(reverse("item",args=(id,)))

@login_required(login_url='login')
def watchlists(request):
    try:
        return render(request,"auctions/watchlist.html",{
                    "bidlist":listing.objects.filter(watcher=request.user,closed=False)
                })
    except:
        return render(request,"auctions/watchlist.html")