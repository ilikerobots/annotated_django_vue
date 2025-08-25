from django.db import models
from rpgdice.choices import ICON_CHOICES


class DicePreset(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    dice_notation = models.CharField(max_length=50)
    icon = models.CharField(max_length=32, choices=ICON_CHOICES, blank=True)

    def __str__(self) -> str:
        return f"{self.name}: {self.dice_notation}"
