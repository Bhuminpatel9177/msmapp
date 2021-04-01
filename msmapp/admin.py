from django.contrib import admin
from msmapp.models import (
    payment1,
    wishlists,
    history,
    carts,
    products,
    subcategories,
    categories,
    Register,
    contact,
    checkout,
)


# Register your models here.
admin.site.register(Register)
admin.site.register(categories)
admin.site.register(subcategories)
admin.site.register(products)
admin.site.register(carts)
admin.site.register(history)
admin.site.register(wishlists)
admin.site.register(checkout)
admin.site.register(payment1)
admin.site.register(contact)
