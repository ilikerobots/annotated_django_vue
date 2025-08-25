from django.contrib import admin
from django.urls import path

from rpgdice import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path("admin/", admin.site.urls),
    path('dice/', views.DicePresetListView.as_view(), name='dice-preset-list'),
    path('dice/<int:pk>/roll', views.RollDiceView.as_view(), name='dice-preset-roll'),
    path('dice/key', views.RollKeyPartialView.as_view(), name='dice-key'),

]
