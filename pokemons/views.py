from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from pokemons.models import Pokemon
from pokemons.serializers import PokemonSerializer


# Create your views here.
class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page"


class PokemonList(generics.ListCreateAPIView):
    # queryset = Pokemon.objects.prefetch_related('types').all()

    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

    """
    List all pokemons, or create a new pokemon.
    """
    def get(self, request, *args, **kwargs):
        type = self.request.query_params.get('type', None)

        if type is not None:
            self.queryset = self.queryset.filter(types__contains=type)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PokemonDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

    """
    Retrieve, update or delete a code pokemon.
    """
    def get(self, request, *args, **kwargs):
        """
        遞迴這種做法可能還有些問題要解，例如：多個子代擁有同一個父代怎麼表示
        但只是 Demo 所以就只是單純用遞迴查詢出來

        另外一種實作可能可以用另外一個表格紀錄 pokemon 間的進化關係，
        然後當 Pokemon 資料產生變化並影響到進化關係時回來維護這張表

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pk = self.kwargs.get('pk')

        # Looking for the next generation
        rawqueryset = Pokemon.objects.raw(f'''
            WITH RECURSIVE ancestors(id, number, name, types, parent_id) AS (
                    SELECT p1.id, p1.number, p1.name, p1.types, p1.parent_id
                    FROM pokemons_pokemon p1
                    WHERE id = {pk}
                UNION ALL
                    SELECT p2.id, p2.number, p2.name, p2.types, p2.parent_id
                    FROM pokemons_pokemon p2
                    JOIN ancestors ON ancestors.id = p2.parent_id
            )
            SELECT id FROM ancestors OFFSET 1;
        ''')

        evolutions = list(map(lambda e: {'id': e.id, 'number': e.number, 'name': e.name, 'types': e.types}, rawqueryset))

        serializer = PokemonSerializer(self.get_object())

        newdict = {'evolutions:': evolutions}
        newdict.update(serializer.data)

        return Response(newdict, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        parentid = request.data['parent_id']

        if parentid is not None:
            if int(pk) == int(parentid):
                return Response(status=HTTP_400_BAD_REQUEST)

            parent = Pokemon.objects.get(pk=parentid)

            if parent is None:
                return Response(status=HTTP_404_NOT_FOUND)

            parentid = parent.id

        pokemon = Pokemon.objects.get(pk=pk)
        if pokemon is None:
            return Response(status=HTTP_404_NOT_FOUND)

        pokemon.parent_id = parentid
        pokemon.save()

        serializer = PokemonSerializer(pokemon)

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        """
        2.刪除寶可夢需求為 「Delete a Pokemon by identifier」，故僅需帶入identifier資訊即可
        然而一個寶可夢有可能是別的寶可夢的進化型，所以需要確保DB的完整性，讓被刪除的寶可夢不會出現在別的寶可夢的進化清單中。

        我這邊是用遞迴查子代，所以刪除掉某個節點後，該節點後面的資料就不會出現在進化清單上了，算是達到這個效果
        不過我覺得也可以用另外一個方式確保 DB 資料的完整性：在刪除前檢查該神奇寶貝是否為其他神奇寶貝的父代(只能刪除最後一代)

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        p = self.get_object()

        self.destroy(request, *args, **kwargs)

        return Response(data={'id': p.id, 'number': p.number, 'name': p.name, 'types': p.types}, status=status.HTTP_204_NO_CONTENT)
