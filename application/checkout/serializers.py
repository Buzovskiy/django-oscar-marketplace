from rest_framework import serializers


class PaymentIntentSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField()
    carrier = serializers.CharField(required=False, allow_null=True)
    products = serializers.CharField()
    shippingDetails = serializers.CharField()
    sessionId = serializers.CharField()
