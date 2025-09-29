# Pokedex Django

Este projeto é uma Pokédex desenvolvida com Django e Django REST Framework, que consome dados da [PokeAPI](https://pokeapi.co/). Ele permite listar, visualizar detalhes e explorar informações dos pokémons de forma moderna e responsiva.

## Funcionalidades
- Listagem dos pokémons com imagem, tipos e número
- Visualização detalhada de cada pokémon (status, habilidades, descrição, altura, peso)
- Interface web responsiva com Bootstrap
- API REST para consulta dos dados
- Carregamento rápido usando requisições paralelas ou assíncronas

## Tecnologias
- Python 3
- Django
- Django REST Framework
- Bootstrap 5
- PokeAPI

## Como rodar
1. Clone o repositório
2. Crie e ative um ambiente virtual
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute as migrações:
   ```bash
   python manage.py migrate
   ```
5. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```
6. Acesse em [http://localhost:8000/pokemon-list/](http://localhost:8000/pokemon-list/)

## Estrutura
- `app/` - Configuração principal do Django
- `pokedex/` - App com views, serializers e urls
- `templates/` - HTMLs responsivos para listagem e detalhes

### Rotas do Frontend
- `/pokemon-list/` — Listagem dos pokémons
- `/pokemon-detail/<id>/` — Detalhes do pokémon selecionado

## Como rodar com Docker

1. Certifique-se de ter o Docker instalado em sua máquina.
2. Construa a imagem do projeto:
   ```bash
   docker build -t pokedex-django .
   ```
3. Execute o container:
   ```bash
   docker run -p 8000:8000 pokedex-django
   ```
4. Acesse em [http://localhost:8000/pokemon-list/](http://localhost:8000/pokemon-list/)

> Se precisar rodar migrações manualmente, utilize:
> ```bash
> docker run pokedex-django python manage.py migrate
> ```


