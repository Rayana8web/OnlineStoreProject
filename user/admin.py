from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('email', 'username', 'is_admin', 'role', 'balance')
    list_filter = ('is_admin', 'role')
    search_fields = ('email', 'username')
    ordering = ('email',)

# Register your models here.
admin.site.register(MyUser, MyUserAdmin)