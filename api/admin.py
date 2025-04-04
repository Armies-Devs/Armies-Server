from django.contrib import admin

from api.models.user import User
from api.models.game_state import GameState

# Register your models here.
@admin.register(User, GameState)
class ArmiesAdmin(admin.ModelAdmin):
    pass