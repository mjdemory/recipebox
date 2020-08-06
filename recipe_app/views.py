from django.shortcuts import render
from recipe_app.models import Recipe, Author
# Create your views here.


def index(request):
    my_recipes = Recipe.objects.all()
    return render(request, "index.html", {"name": "Kenzie", "recipes": my_recipes})


def post_detail(request, post_id):
    my_recipe = Recipe.objects.filter(id=post_id).first()
    return render(request, "post_detail.html", {"post": my_recipe})


def author_detail(request, author_id):
    author_recipes = Recipe.objects.filter(author__id=author_id)
    author_info = Author.objects.get(id=author_id)
    return render(request, "author_detail.html", {"author": author_recipes, "name": author_info.name, "bio": author_info.bio})
