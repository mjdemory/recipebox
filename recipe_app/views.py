from django.shortcuts import render, HttpResponseRedirect, reverse
from recipe_app.models import Recipe, Author
from recipe_app.forms import AddRecipeForm, AddAuthorForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django import forms

# Create your views here.


def index(request):
    my_recipes = Recipe.objects.all()
    return render(request, 'index.html', {'recipes': my_recipes})


def post_detail(request, post_id):
    my_recipe = Recipe.objects.filter(id=post_id).first()
    return render(request, 'post_detail.html', {'post': my_recipe})


def author_detail(request, author_id):
    author_recipes = Recipe.objects.filter(author__id=author_id)
    author_info = Author.objects.filter(id=author_id).first()
    favorites_list = author_info.favorite.all()
    return render(request, 'author_detail.html', {'author': author_recipes, 'favorites': favorites_list, 'author_info': author_info})


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                time_required=data.get('time_required'),
                instructions=data.get('instructions'),
                author=data.get('author'),
            )
            return HttpResponseRedirect(reverse('homepage'))

    form = AddRecipeForm()
    if not request.user.is_staff:
        form.fields['author'] = forms.ModelChoiceField(
            queryset=Author.objects.filter(name=request.user.author))
    return render(request, 'recipe_form.html', {'form': form})


@login_required
def recipe_edit_view(request, post_id):
    post = Recipe.objects.get(id=post_id)
    if request.user.is_staff or request.user.author.id == post.author.id:
        if request.method == "POST":
            form = AddRecipeForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                post.title = data["title"]
                post.description = data["description"]
                post.time_required = data["time_required"]
                post.instructions = data["instructions"]
                post.author = data["author"]
                post.save()
                return HttpResponseRedirect(reverse('post_detail', args=[post.id]))

        data = {
            "title":post.title,
            "description": post.description,
            "time_required": post.time_required,
            "instructions": post.instructions,
            "author": post.author
        }
        form = AddRecipeForm(initial=data)
        return render(request, "basic_form.html", {'form':form})
    return HttpResponseRedirect(reverse('homepage'))

@login_required
@staff_member_required
def add_author(request):
    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data.get(
                'username'), password=data.get('password'))
            new_author = form.save(commit=False)
            new_author.user = new_user
            new_author.save()
            return HttpResponseRedirect(reverse('homepage'))

    form = AddAuthorForm()
    return render(request, 'author_form.html', {'form': form})


def favorite_view(request, fav_id):
    # Detrich and Peter code
    current_author = Author.objects.filter(user__id=request.user.id).first()
    add_favorite_recipe = Recipe.objects.filter(id=fav_id).first()
    current_author.favorite.add(add_favorite_recipe)
    current_author.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def unfavorite_view(request, unfav_id):
    current_author = Author.objects.filter(user__id=request.user.id).first()
    remove_favorite_recipe = Recipe.objects.filter(id=unfav_id).first()
    current_author.favorite.add(remove_favorite_recipe)
    current_author.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data.get('username'),
                                password=data.get('password'))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse('homepage')))

    form = LoginForm()
    return render(request, 'login_form.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
