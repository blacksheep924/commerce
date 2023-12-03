from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import Newitem
from .models import User, Product, Bid, Comments
from django.db.models import Max

def index(request):
    products = Product.objects.all()
    prices = Product.objects.filter(productprice__amount__gt=0)
    
    


    
    
    
        
    
    
        
       
   
    
    





    return render(request, "auctions/index.html",{'products' : products, 'prices':prices})


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
    image = productname.productImage
    
    bids = Bid.objects.filter(product = productname)
    prices = [bid.bidPrice for bid in bids]
    prices.sort(reverse = True)
    price = prices[0]
    if request.method == "POST":
        name = product_name
        

        new_bid = float(request.POST.get('newbid'))
        newprice = float(price)
        if new_bid <= newprice:
            return render(request, "auctions/productdetail.html", {'productname': name, 'username' : username, 'image' : image, 'price' : price, 'message': "Bid too low"})
        else:
            current_bid = new_bid

            new_product = Product(
                productOwner = request.user,
                productName = productname,   
                productImage = image

            )
            
            
            try:
                existing_product = Product.objects.get(productName=name, productOwner=request.user, productImage=image)
                make_bid = Bid(
                    bidPrice=current_bid,
                    bidder=request.user,
                    product=existing_product
                )
                make_bid.save()
            except Product.DoesNotExist:
                new_product = Product(
                    productName=name,
                    productOwner=request.user,
                    productImage=image
                )
                new_product.save()

                make_bid = Bid(
                    bidPrice=current_bid,
                    bidder=request.user,
                    product=new_product
                )
                make_bid.save()

            return  redirect('index')
             
        

        
    else:

        return render (request, "auctions/productdetail.html",{'productname' : product_name, 'username' : username, 'image' : image, 'price' : price})

        
