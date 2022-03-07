from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Hobby)
admin.site.register(HobbyComment)
admin.site.register(HobbyLiked)