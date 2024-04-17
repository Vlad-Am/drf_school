from rest_framework import serializers

from users.models import User, Pays


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = '__all__'
