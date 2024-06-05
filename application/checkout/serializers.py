from rest_framework import serializers


class PaymentIntentSerializer(serializers.Serializer):
    carrier = serializers.CharField(required=False, allow_null=True)
    shippingDetails = serializers.CharField()
