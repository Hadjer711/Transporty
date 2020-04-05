from django.contrib import admin

# Register your models here.

from .models import AnnonceMarchandise, AnnonceTrajet, Affectation

from .models import User

admin.site.site_header = "Administration du site TRANSPORTY"


admin.site.register(User)
admin.site.register(AnnonceMarchandise)
admin.site.register(AnnonceTrajet)
admin.site.register(Affectation)