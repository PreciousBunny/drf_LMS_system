from rest_framework import serializers

from users.models import User
from course.models import Payment


class UserPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    all_payment = UserPaymentSerializer(source='payment_set', many=True, read_only=True,)

    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'city', 'all_payment',)
