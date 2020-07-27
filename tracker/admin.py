from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'time_created', 'sport', 'holes', 'getTs')

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Sport)
admin.site.register(HolesNumber)
admin.site.register(Game, GameAdmin)
admin.site.register(Score9)
admin.site.register(Score18)
