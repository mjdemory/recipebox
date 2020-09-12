"""recipebox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recipe_app import views as v


urlpatterns = [
    path('', v.index, name="homepage"),
    path('recipeindex/', v.index, name="recipe_index"),
    path('post/<int:post_id>/edit/', v.recipe_edit_view), 
    path('post/<int:post_id>/', v.post_detail, name="post_detail"),
    path('author/<int:author_id>/', v.author_detail),
    path('addrecipe/', v.add_recipe, name="addrecipe"),
    path('addauthor/', v.add_author, name="addauthor"),
    path('login/', v.login_view, name="login_view"),
    path('logout/', v.logout_view, name="logout_view"),
    path('favorite_view/<int:fav_id>/', v.favorite_view, name="favorite"),
    path('unfavorite_view/<int:unfav_id>/', v.unfavorite_view, name="unfavorite"),
    path('admin/', admin.site.urls),
]
