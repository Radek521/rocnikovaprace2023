from django.contrib import admin

from .models import Mistnost, Tema, Zprava

admin.site.register(Mistnost)
admin.site.register(Tema)
admin.site.register(Zprava)