from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'email_confirmed', 'reset_password')

class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'time_created', 'sport', 'holes', 'getTs')

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Sport)
admin.site.register(HolesNumber)
admin.site.register(Game, GameAdmin)
admin.site.register(Score9)
admin.site.register(Score18)
