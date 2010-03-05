from django.contrib import admin
from animals.models import Animal


class AnimalAdmin(admin.ModelAdmin):
    pass

admin.site.register(Animal, AnimalAdmin)
