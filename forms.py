from django.forms import ModelForm
from .models import Mistnost

class MistnostForm(ModelForm):
    class Meta:
        model = Mistnost
        fields = '__all__'
        