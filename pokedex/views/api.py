from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from pokedex.serializers import PokemonDetailSerializer, PokemonListSerializer, PokemonSerializer

# Create your views here.


class PokedexListAPIView(APIView):

    url = 'https://pokeapi.co/api/v2'
    
    def get(self, request):
        response = requests.get(f'{self.url}/pokemon')
        data = response.json().get('results', [])
        
        obj = PokemonSerializer(data=data, many=True)
        obj.is_valid(raise_exception=True)
        

        list_pokemon = []

        for pokemon in obj.data:
            response_list = requests.get(pokemon.get('url'))
            pokemon_data = response_list.json()

            list_pokemon.append({
                "id": pokemon_data.get("id"),
                "name": pokemon_data.get("name"),
                "types": [t["type"]["name"] for t in pokemon_data.get("types")],
                "sprite": pokemon_data.get("sprites").get("front_default")
            })

        serializer_pokemon = PokemonListSerializer(data=list_pokemon, many=True)
        serializer_pokemon.is_valid(raise_exception=True)

        return Response({'result': serializer_pokemon.validated_data})
    

class PokedexDetailAPIView(APIView):

    url = 'https://pokeapi.co/api/v2'

    def get(self, request, pokemon_id):
        response_detail = requests.get(f'{self.url}/pokemon/{pokemon_id}/')

        response_detail_species = requests.get(f'{self.url}/pokemon-species/{pokemon_id}/')

        data_species = response_detail_species.json()

        data = response_detail.json()
  


        serializer_detail = {
            "id": data.get("id"),
            "name": data.get("name"),
            "height": data.get("height"),
            "weight": data.get("weight"),
            "types": [t["type"]["name"] for t in data.get("types")],
            "sprite": data.get("sprites").get("front_default"),
            "status": [{status["stat"]["name"]: status["base_stat"]} for status in data.get("stats")],
            "abilities": [a["ability"]["name"] for a in data.get("abilities")],
            "species_description": data_species.get('flavor_text_entries', [])[0].get('flavor_text'),
        }

        serializer_pokemon_detail = PokemonDetailSerializer(data=serializer_detail)
        serializer_pokemon_detail.is_valid(raise_exception=True)

        return Response({'result': serializer_pokemon_detail.validated_data})