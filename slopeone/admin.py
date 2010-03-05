from django.contrib import admin
from slopeone.models import Rating


class RatingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Rating, RatingAdmin)
