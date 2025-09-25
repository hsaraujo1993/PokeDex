from rest_framework import serializers


class PokemonSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    url = serializers.URLField()


class PokemonListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    types = serializers.ListField(child=serializers.CharField(max_length=50))
    sprite = serializers.URLField()


class PokemonDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    height = serializers.IntegerField()
    weight = serializers.IntegerField()
    types = serializers.ListField(child=serializers.CharField(max_length=50))
    sprite = serializers.URLField()
    status = serializers.ListField(child=serializers.DictField())
    abilities = serializers.ListField(child=serializers.CharField(max_length=100))
    species_description = serializers.CharField()

