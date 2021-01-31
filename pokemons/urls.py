from django.urls import path
from pokemons import views

urlpatterns = [
    path('', views.PokemonList.as_view()),
    path('<int:pk>', views.PokemonDetail.as_view()),
]