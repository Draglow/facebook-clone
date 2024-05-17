from django.contrib import admin
from core.models import Gallery,History,Post,FriendRequest,Comment,Friend,ReplyComment,Notification,Page,PagePost,Group,GroupPost,ChatMessage
from django.utils.html import format_html
# Register your models here.

class GalleryAdminTap(admin.TabularInline):
    model=Gallery
    
    
class PostGallery(admin.ModelAdmin):
    inlines=[GalleryAdminTap]
    def thumbnail(self,object):
        return format_html("<img src='{}' width='40' style='border-radius:50px;' />".format(object.image.url))
    thumbnail.short_discription='image'
    list_editable=['active']
    list_display=['thumbnail','user','title','visibility','active']
    prepopulated_fields={'slug':('title',)}
    
    
class AdminGallery(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html("<img src='{}' width='40' style='border-radius:50px;' />".format(object.image.url))
    thumbnail.short_discription='image'
    list_editable=['active']
    list_display=['id','post','thumbnail','active']
    list_display_links=['id','post','thumbnail']


class AdminFriendRequest(admin.ModelAdmin):
    
    list_editable=['status']
    list_display=['sender','receiver','status']
    list_display_links=['sender','receiver']
    
class AdminFriend(admin.ModelAdmin):
    
    
    list_display=['user','friend']
    list_display_links=['user','friend']


class Admincomment(admin.ModelAdmin):
    
    
    list_display=['user','post','comment','active']
    list_display_links=['user','post']


class Adminreply(admin.ModelAdmin):
    
    
    list_display=['user','comment','active']
    list_display_links=['user','comment','active']


class AdminNotification(admin.ModelAdmin):
    list_display=['user', 'post', 'sender', 'notification_type', 'comment', 'is_read']

    #list_display_links=('user','post','sender','notification_type')
class GroupPostTab(admin.TabularInline):
    model=GroupPost
    
class adminPage(admin.ModelAdmin):
    list_editable=['user','name','visibility']
    list_display=['thumbnail','user','name','name','visibility']
    list_display_links=['thumbnail','user','name','name','visibility']


class adminGroup(admin.ModelAdmin):
    inlines=[GroupPostTab]
    list_editable=['user','name','visibility']
    list_display=['thumbnail','user','name','visibility']
    prepopulated_fields={'slug':('name',)}
    list_display_links=['thumbnail','user','name','name','visibility']
    

class adminPage(admin.ModelAdmin):
    list_editable=['user','name','visibility']
    list_display=['thumbnail','user','name','name','visibility']
    list_display_links=['thumbnail','user','name','name','visibility']


class ChatMessageAdmin(admin.ModelAdmin):
    
   
    list_display=['sender','receiver','message','is_read']
    list_editable=['message'] 

admin.site.register(Gallery,AdminGallery)
admin.site.register(Post,PostGallery)
admin.site.register(FriendRequest,AdminFriendRequest)
admin.site.register(Comment,Admincomment)
admin.site.register(Friend,AdminFriend)
admin.site.register(ReplyComment,Adminreply)
admin.site.register(Notification)
admin.site.register(Group)
admin.site.register(GroupPost)
admin.site.register(Page)
admin.site.register(PagePost)
admin.site.register(History)
admin.site.register(ChatMessage,ChatMessageAdmin)
