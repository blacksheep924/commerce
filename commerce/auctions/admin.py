from django.contrib import admin
from.models import User, Product, Bid, Comments

# Register your models here.
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Product)
admin.site.register(Comments)
