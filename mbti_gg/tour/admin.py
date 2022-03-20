from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Tour)
admin.site.register(TourComment)
admin.site.register(TourLiked)