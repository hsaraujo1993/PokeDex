from django.shortcuts import render

def pokemon_list_page(request):
    return render(request, "list.html")


def pokemon_detail_page(request, pokemon_id):
    return render(request, "detail.html", {"pokemon_id": pokemon_id})