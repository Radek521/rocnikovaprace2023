from django.db import models
from django.contrib.auth.models import User

class Tema(models.Model):
    jmeno = models.CharField(max_length=200)

    def __str__(self):
        return str(self.jmeno)

#vytvoreni modelu
class Mistnost(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True)
    jmeno = models.CharField(max_length=200)
    popis = models.TextField(null=True, blank=True)
    ucastnici = models.ManyToManyField(User, related_name='ucastnici', blank=True)
    aktualizovano = models.DateTimeField(auto_now=True)
    vytvoreno = models.DateTimeField(auto_now_add=True)

#serazeni mistnosti od nejnovejsich po nejstarsich
    class Meta:
        ordering = ['-aktualizovano','-vytvoreno']

#tato metoda vrací textovou reprezentaci atributu jmeno objektu
    def __str__(self):
        return str(self.jmeno)

class Zprava(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mistnost = models.ForeignKey(Mistnost, on_delete=models.CASCADE)
    zprava = models.TextField()
    aktualizovano = models.DateTimeField(auto_now=True)
    vytvoreno = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-aktualizovano','-vytvoreno']

    def __str__(self):
        return self.zprava[0:50]