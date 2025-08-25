from django.contrib import admin

from .models import DicePreset


@admin.register(DicePreset)
class DicePresetAdmin(admin.ModelAdmin):
    list_display = ("name", "dice_notation", "icon")
    search_fields = ("name", "dice_notation", "description")
    ordering = ("name",)
