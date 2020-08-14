from django.shortcuts import render, HttpResponseRedirect, reverse
from recipe_app.models import Recipe, Author
from recipe_app.forms import AddRecipeForm, AddAuthorForm, LoginForm, SignupForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

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
    return render(request, 'author_detail.html', {'author': author_recipes, 'author_info': author_info})


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
                author=request.user.author,
            )
            return HttpResponseRedirect(reverse('homepage'))

    form = AddRecipeForm()
    return render(request, 'recipe_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def add_author(request):
    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('homepage'))

    form = AddAuthorForm()
    return render(request, 'author_form.html', {'form': form})


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


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data.get(
                'username'), password=data.get('password'))
            Author.objects.create(name=data.get(
                'username'), bio=data.get('bio'), user=new_user)
            login(request, new_user)
            return HttpResponseRedirect(reverse('homepage'))

    form = SignupForm()
    return render(request, 'signup_form.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
