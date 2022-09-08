from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import MenuItem, Ingredient, RecipeRequirements, Purchase
from .forms import PurchaseCreateForm


# Create your views here.
class SignUp(CreateView):
    template_name = "menu/registration/signup.html"
    success_url = reverse_lazy("login")
    form_class = UserCreationForm

#1st user
#username="Pablo", email="pablo@wildesteak.com", password="steak123"

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        #try:
        #    user = User.objects.get(username=username)
        #except:
        #    messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password does not exist")
    context = {}
    return render(request, "menu/registration/login.html")

def logoutPage(request):
    logout(request)
    return redirect('home')


def home(request):
    return render(request, "menu/home.html")

class MenuItemList(ListView):
    template = "menu/menuitem_list.html"
    model = MenuItem


class MenuItemCreate(LoginRequiredMixin, CreateView):
    model = MenuItem
    template_name = "menu/menuitem_create_form.html"
    fields = ["title", "price"]
    login_url = "login"

class IngredientList(ListView):
    template_name = "menu/ingredient_list.html"
    model = Ingredient


class IngredientCreate(LoginRequiredMixin, CreateView):
    template_name = "menu/ingredient_create_form.html"
    model = Ingredient
    fields = ["name", "quantity", "unit", "unit_price"]
    login_url = "login"

class IngredientDelete(LoginRequiredMixin, DeleteView):
    template_name = "menu/ingredient_delete_form.html"
    model = Ingredient
    login_url = "login"

class IngredientUpdate(LoginRequiredMixin, UpdateView):
    template_name = "menu/ingredient_update_form.html"
    model = Ingredient
    fields = ["name", "quantity", "unit", "unit_price"]
    login_url = "login"

class RecipeList(ListView):
    template_name = "menu/recipe_list.html"
    model = RecipeRequirements

class RecipeCreate(LoginRequiredMixin, CreateView):
    template_name = "menu/recipe_create_form.html"
    model = RecipeRequirements
    fields = ["menu_item", "ingredient", "quantity"]
    login_url = "login"

class PurchaseView(ListView):
    template_name = "menu/purchases_list.html"
    model = Purchase
    #function to use to get context ot be used
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        purchases = Purchase.objects.all()
        sum = 0
        total_cost = 0
        # recipe.quantity * ingredient.unit_price

        for purchase in purchases:
            sum += purchase.menu_item.price
            recipes = RecipeRequirements.objects.filter(menu_item=purchase.menu_item)
            for recipe in recipes:
                ingred = Ingredient.objects.get(id=recipe.ingredient.id)
                total_cost += recipe.quantity * ingred.unit_price
        profit = sum - total_cost
        data['sum'] = sum
        data['total_cost'] = total_cost
        data['profit'] = profit
        return data

@login_required(login_url="login")
def PurchaseCreate(request):
    form = PurchaseCreateForm()
    context = {"form": form}
    if request.method == "POST":
        form = PurchaseCreateForm(request.POST)
        if form.is_valid():
            purchase = form.save()
            #Line that gives recipe objects
            recipe = RecipeRequirements.objects.filter(menu_item=request.POST.get("menu_item"))
            #extracting quantiyty needed to be subtracted from inventory numbers
            for elem in recipe:
                ingr = Ingredient.objects.get(id=elem.ingredient.id)
                if ingr.quantity > elem.quantity:
                    ingr.quantity = ingr.quantity - elem.quantity
                    ingr.save()
            return redirect('purchases')

    return render(request, "menu/purchase_create_form.html", context)