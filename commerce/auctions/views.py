from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import Newitem
from .models import User, Product, Bid, Comments, Watchlist
from django.db.models import Max

def index(request):
    
    products = Product.objects.all()
    username =  request.user

    

    
    
    

    

        
        

    
        
    return render(request, "auctions/index.html",{'products' : products, 'username' : username})


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

@login_required   
def newlisting(request):
    form = Newitem()
    
    if request.method == "POST":
       form = Newitem(request.POST)
       if form.is_valid():
           new_item = Product(
               productOwner = request.user,
               productName = form.cleaned_data['item'],    
               productImage = form.cleaned_data['image'],
               productCategory = form.cleaned_data['category']
               
           )
           
           new_item.save()

           new_bid = Bid(
               bidPrice = form.cleaned_data['startbid'],
               bidder = request.user,
               product=new_item
               
           )
           
           new_bid.save()

           new_description = Comments(
               commentcontent = form.cleaned_data['description'],
               commentator = request.user,
               product=new_item
               
           )

           new_description.save()

           return redirect('index')
    
    else:


        return render(request, "auctions/newlisting.html", {'form' : form})
    
@login_required 
def productdetail(request, product_name):
    
    productname = Product.objects.get(productName=product_name)
    username = productname.productOwner.username
    user_product = User.objects.get(username = productname.productOwner.username)
    id = user_product.id
    image = productname.productImage
    category = productname.productCategory

    comments = Comments.objects.filter(product = productname)
    
    bids = Bid.objects.filter(product = productname)
    
    prices = [bid.bidPrice for bid in bids]
    prices.sort(reverse = True)
    price = prices[0]
    highest_bidder = Bid.objects.filter(product = productname)
    if request.method == "POST":
        if 'placebid' in request.POST:
            name = product_name

            new_bid = (request.POST.get('newbid'))
            
            new_bid = float(new_bid)
            newprice = float(price)

            if new_bid <= newprice:

                return render(request, "auctions/productdetail.html", {'productname': name, 'username' : username, 'image' : image, 'price' : price, 'message': "Bid too low", 'comments': comments})
            
            else:

                current_bid = new_bid
                existing_product = Product.objects.get(productName=name, productOwner=id, productImage=image, productCategory = category)
                make_bid = Bid(
                    bidPrice=current_bid,
                    bidder=request.user,
                    product=existing_product
                )
                make_bid.save()
                
                return  redirect('index')
        if 'comments' in request.POST:
            name = product_name
            existing_product = Product.objects.get(productName=name, productOwner=id, productImage=image, productCategory = category)
            make_comment = Comments(
               commentcontent = request.POST.get('commentcontent'),
               commentator = request.user,
               product = existing_product
            )
            make_comment.save()

            return render (request, "auctions/productdetail.html",{'productname' : product_name, 'username' : username, 'image' : image, 'price' : price, 'category' : category, 'comments': comments})
            
        if 'close_auction' in request.POST:
            name = product_name
            winner = request.POST.get('Winner')
            winner_username = User.objects.get(username = winner)
            
            

            save_product = Product.objects.get(productName=name)
            save_product.productListed = False
            save_product.productWinner = winner_username

            save_product.save()

            return redirect('index')
            

            

    
        
             
        
    
        
    else:
        user = request.user.id
        winner = Product.objects.filter(productName = product_name)
        
        return render (request, "auctions/productdetail.html",{ 'winner': winner, 'productname' : product_name, 'username' : username, 'image' : image, 'price' : price, 'category' : category, 'comments': comments, 'bidder' : highest_bidder})

@login_required
def watchlist(request):
    username = request.user
    
    if request.method == "POST":
        if 'tickbox1' in request.POST:
            productname = request.POST.get('watchlistProduct1')
            watchlist_check = request.POST.get('tickbox1')
            

            watchlist_user = username
            save_product = Product.objects.get(productName=productname)
            save_username = User.objects.get(username = watchlist_user)
            make_watchlist = Watchlist(
                watchlistUser = save_username,
                watchlistProduct = save_product,
                watchlistShow = watchlist_check
            )
            existing_watchlist = Watchlist.objects.filter(watchlistProduct = save_product, watchlistUser = save_username)
            if existing_watchlist:
                existing_watchlist = Watchlist.objects.get(watchlistProduct = save_product, watchlistUser = save_username)
                existing_watchlist.watchlistShow = watchlist_check
                existing_watchlist.save()
            else:
                make_watchlist.save()

            return redirect('index')
        
        elif 'tickbox2' in request.POST:
            productname = request.POST.get('watchlistProduct2')
            watchlist_check = request.POST.get('tickbox2')

            watchlist_user = username
            save_product = Product.objects.get(productName=productname)
            save_username = User.objects.get(username = watchlist_user)
            make_watchlist = Watchlist(
                watchlistUser = save_username,
                watchlistProduct = save_product,
                watchlistShow = watchlist_check
            )
            existing_watchlist = Watchlist.objects.filter(watchlistProduct = save_product, watchlistUser = save_username)
            if existing_watchlist:
                existing_watchlist = Watchlist.objects.get(watchlistProduct = save_product, watchlistUser = save_username)
                existing_watchlist.watchlistShow = watchlist_check
                existing_watchlist.save()
            else:
                make_watchlist.save()

            return redirect('index')
        
    watchlistobjects = Watchlist.objects.all()

    return render(request, "auctions/watchlist.html",{'watchlistobjects' :watchlistobjects}) 

@login_required
def categories(request):
    categories = Product.objects.all()
    return render(request, "auctions/categories.html", {'categories' : categories}) 

@login_required
def category(request, category):
    query = category
    objects = Product.objects.filter(productCategory = query)
    

    return render(request, "auctions/category.html",{'objects' : objects})

