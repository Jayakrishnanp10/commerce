from django.contrib import admin

from .models import bid,comment,listing,bid
# Register your models here.

admin.site.register(bid)
admin.site.register(comment)
admin.site.register(listing)
