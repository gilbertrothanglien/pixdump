from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(upload_image)
admin.site.register(image_like)
admin.site.register(follows)
admin.site.register(image_comments)