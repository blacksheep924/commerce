from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path('auctions/<str:product_name>/', views.productdetail, name="product_name"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path('auctions/categories/<str:category>/',views.category, name="category")
]
