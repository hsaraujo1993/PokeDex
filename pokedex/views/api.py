from functools import cache
from django.shortcuts import render
from django.core.cache import cache
from django.core.paginator import Paginator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
import requests
import logging

from pokedex.serializers import PokemonDetailSerializer, PokemonListSerializer

# Create your views here.


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PokedexListAPIView(APIView):
    url = 'https://pokeapi.co/api/v2'
    cache_timeout = 60 * 2  # 2 minutos

    def get(self, request):
        offset = int(request.query_params.get('offset', 0))
        limit = int(request.query_params.get('limit', 20))

        cache_key = f'pokedex_list_{offset}_{limit}'
        data = cache.get(cache_key)

        if data is None:
            logger.info("Cache MISS para chave: %s", cache_key)

            try:
                response = requests.get(f'{self.url}/pokemon', params={'offset': offset, 'limit': limit})
                response.raise_for_status()
                results = response.json().get('results', [])
                data = self._build_pokemon_list(results)
                serializer = PokemonListSerializer(data=data, many=True)
                serializer.is_valid(raise_exception=True)
                data = serializer.validated_data
                cache.set(cache_key, data, self.cache_timeout)

            except requests.RequestException as e:
                logger.error(f'Erro ao buscar dados da Pokédex: {e}')
                return Response({'error': 'Não foi possível obter os dados da Pokédex.'}, status=503)

        else:
            logger.info("Cache HIT para chave: %s", cache_key)

        return Response({
            "count": len(data),
            "next": f"/api/v1/pokemon/?offset={offset + limit}&limit={limit}",
            "previous": f"/api/v1/pokemon/?offset={max(offset - limit, 0)}&limit={limit}" if offset > 0 else None,
            "results": data
        })


    def _build_pokemon_list(self, results):

        return [
            {
                "id": (pokemon_data := requests.get(pokemon.get('url')).json()).get("id"),
                "name": pokemon_data.get("name"),
                "types": [t["type"]["name"] for t in pokemon_data.get("types")],
                "sprite": pokemon_data.get("sprites", {}).get("front_default")
            }
            for pokemon in results
        ]
    

class PokedexListTypeAPIView(APIView):
    url = 'https://pokeapi.co/api/v2'

    cache_timeout = 60 * 2  # 2 minutos

    def get(self, request):

        cache_key = 'pokedex_types'
        data = cache.get(cache_key)

        if data is None:
            logger.info("Cache MISS para chave: %s", cache_key)
            try:
                response = requests.get(f'{self.url}/type')
                response.raise_for_status()
                results = response.json().get('results', [])
                data = self._build_pokemon_list_type(results)
                cache.set('pokedex_types', data, self.cache_timeout)
            except requests.RequestException as e:
                logger.error(f'Erro ao buscar tipos de Pokémon: {e}')
                return Response({'error': 'Não foi possível obter os tipos de Pokémon.'}, status=503)
        else:
            logger.info("Cache HIT para chave: %s", cache_key)

        return Response({'results': data})

    def _build_pokemon_list_type(self, results):
        return [
            {   
                "type": type_data.get("name"),
                "id": type_data.get("url", "").rstrip('/').split('/')[-1]
            }
            for type_data in results
        ]
    

class PokedexListPokemonTypeAPIView(APIView):
    url = 'https://pokeapi.co/api/v2'

    cache_timeout = 60 * 2  # 2 minutos

    def get(self, request, id):

        cache_key = f'pokedex_type_{id}'
        data = cache.get(cache_key)

        if data is None:
            logger.info("Cache MISS para chave: %s", cache_key)
            try:
                response = requests.get(f'{self.url}/type/{id}')
                response.raise_for_status()
                results = response.json().get('pokemon', [])
                data = self._build_pokemon_list(results)
                cache.set(cache_key, data, self.cache_timeout)
            except requests.RequestException as e:
                logger.error(f'Erro ao buscar Pokémon por tipo: {e}')
                return Response({'error': 'Não foi possível obter os Pokémon por tipo.'}, status=503)
        else:
            logger.info("Cache HIT para chave: %s", cache_key)

        return Response({'results': data})


    def _build_pokemon_list(self, results):
        return [
        {
        "id": (pokemon_data := requests.get(pokemon["pokemon"]["url"]).json()).get("id"),
        "name": pokemon_data.get("name"),
        "types": [t["type"]["name"] for t in pokemon_data.get("types", [])],
        "sprite": pokemon_data.get("sprites", {}).get("front_default"),
    }
    for pokemon in results
]






class PokedexDetailAPIView(APIView):
    url = 'https://pokeapi.co/api/v2'
    cache_timeout = 60 * 2

    def get(self, request, pokemon_id=None):

        pokemon_name = request.query_params.get('name')

        # Definir a chave de cache dinamicamente
        key = pokemon_name if pokemon_name else pokemon_id
        cache_key = f'pokedex_detail_{key}'

        data = cache.get(cache_key)

        if data is None:
            logger.info("Cache MISS para chave: %s", cache_key)

            try:
                # Decide se busca por ID ou por Nome
                if pokemon_name:
                    response_detail = requests.get(f'{self.url}/pokemon/{pokemon_name.lower()}/')
                    response_detail.raise_for_status()
                    response_species = requests.get(f'{self.url}/pokemon-species/{pokemon_name.lower()}/')
                    response_species.raise_for_status()
                else:
                    response_detail = requests.get(f'{self.url}/pokemon/{pokemon_id}/')
                    response_detail.raise_for_status()
                    response_species = requests.get(f'{self.url}/pokemon-species/{pokemon_id}/')
                    response_species.raise_for_status()

            except requests.RequestException as e:
                logger.error(f'Erro ao buscar dados do Pokémon: {e}')
                return Response({'error': 'Não foi possível obter os dados do Pokémon.'}, status=503)

            pokemon_data = response_detail.json()
            species_data = response_species.json()

            data = self._build_pokemon_detail(pokemon_data, species_data)
            cache.set(cache_key, data, self.cache_timeout)

        else:
            logger.info("Cache HIT para chave: %s", cache_key)

        serializer = PokemonDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response({'result': serializer.validated_data})
    

    def _build_pokemon_detail(self, pokemon_data, species_data):

        flavor_entries = species_data.get('flavor_text_entries', [])
        description = ""
        for entry in flavor_entries:
            if entry.get('language', {}).get('name') == 'en':
                description = entry.get('flavor_text', "")
                break
        if not description and flavor_entries:
            description = flavor_entries[0].get('flavor_text', "")
        return {
            "id": pokemon_data.get("id"),
            "name": pokemon_data.get("name"),
            "height": pokemon_data.get("height"),
            "weight": pokemon_data.get("weight"),
            "types": [t["type"]["name"] for t in pokemon_data.get("types")],
            "sprite": pokemon_data.get("sprites", {}).get("front_default"),
            "status": [{status["stat"]["name"]: status["base_stat"]} for status in pokemon_data.get("stats", [])],
            "abilities": [a["ability"]["name"] for a in pokemon_data.get("abilities", [])],
            "species_description": description,
        }
    



            
    
