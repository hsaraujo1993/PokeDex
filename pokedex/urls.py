from django.urls import path
from .views.api import PokedexListAPIView, PokedexDetailAPIView
from .views.page import pokemon_detail_page, pokemon_list_page

urlpatterns = [
    path('pokemon/', PokedexListAPIView.as_view(), name='pokedex-list'),
    path('pokemon/<int:pokemon_id>/', PokedexDetailAPIView.as_view(), name='pokedex-detail'),

    path("pokemon-list/", pokemon_list_page, name="pokemon-list-page"),
    path("pokemon-detail/<int:pokemon_id>/", pokemon_detail_page, name="pokemon-detail-page"),
]
