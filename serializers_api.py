from rest_framework.serializers import ModelSerializer
from zaklad.models import Mistnost

class MistnostSerializer(ModelSerializer):
    class Meta: 
        model = Mistnost
        fields = '__all__'