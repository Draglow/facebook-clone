from django.contrib import admin
from userauths.models import User
from userauths.models import Profile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=['username','full_name','username','email','gender']
    list_display_links=['full_name','username']
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','full_name','varified']
    list_display_links=['full_name','user']
    list_editable=['varified']

admin.site.register(User,UserAdmin)
admin.site.register(Profile,ProfileAdmin)