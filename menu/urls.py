from django.urls import path, include
from .import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("menu", views.MenuItemList.as_view(), name="menu"),
    path("menu/create", views.MenuItemCreate.as_view(), name="new_item"),
    path("inventory", views.IngredientList.as_view(), name="inventory"),
    path("inventory/create", views.IngredientCreate.as_view(), name="new_ingredient"),
    path("inventory/update/<pk>", views.IngredientUpdate.as_view(), name="ingredient_update"),
    path("inventory/delete/<pk>", views.IngredientDelete.as_view(), name="ingredient_delete"),
    path("purchases", views.PurchaseView.as_view(), name="purchases"),
    path("purchases/create", views.PurchaseCreate, name="new_purchase"),
    path("recipe", views.RecipeList.as_view(), name="recipe"),
    path("recipe/create", views.RecipeCreate.as_view(), name="new_recipe"),
]