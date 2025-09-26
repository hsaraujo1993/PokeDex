from django.urls import path
from .views.api import PokedexListAPIView, PokedexDetailAPIView, PokedexListPokemonTypeAPIView, PokedexListTypeAPIView
from .views.page import pokemon_detail_page, pokemon_list_page

urlpatterns = [
    path('pokemon/', PokedexListAPIView.as_view(), name='pokedex-list'),
    path('pokemon/types/', PokedexListTypeAPIView.as_view(), name='pokedex-type-list'),
    path('pokemon/<pokemon_id>/', PokedexDetailAPIView.as_view(), name='pokedex-detail'),
    path('pokemon/types/<id>/', PokedexListPokemonTypeAPIView.as_view(), name='pokedex-pokemon-type-list'),

    path("pokemon-list/", pokemon_list_page, name="pokemon-list-page"),
    path("pokemon-detail/<pokemon_id>/", pokemon_detail_page, name="pokemon-detail-page"),
]
