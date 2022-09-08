from django.db import models

# Create your models here.
class MenuItem(models.Model):
    title = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/menu"

class Ingredient(models.Model):
    UNITS = [
        ("gram", "g"),
        ("kilogram", "kg"),
        ("piece", "pcs"),
        ("mililitr", "ml"),
        ("litre", "l"),
        ("other", "other")
    ]
    name = models.CharField(max_length=200)
    quantity = models.FloatField(null=True)
    unit = models.CharField(max_length=10, choices=UNITS, default="other")
    unit_price = models.FloatField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/inventory"

class RecipeRequirements(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def get_absolute_url(self):
        return "/recipe"

class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, related_name="menuitem", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return "/purchases"

    def __str__(self):
        return self.menu_item.title
