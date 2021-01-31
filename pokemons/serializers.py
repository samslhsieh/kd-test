from pokemons.models import Pokemon
from rest_framework import serializers


class PokemonSerializer(serializers.ModelSerializer):
    # types = TypeSerializer(many=True)
    # types = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    types = serializers.JSONField()

    class Meta:
        model = Pokemon
        fields = ['id', 'number', 'name', 'types']
