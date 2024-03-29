from django.contrib import admin
from .models import Tour, Tourist, Review, User, Reservation

# Register your models here.
admin.site.register(Tour)
admin.site.register(Tourist)
admin.site.register(Review)
admin.site.register(Reservation)