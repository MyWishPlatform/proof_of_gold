from rest_framework import serializers
from remusgold.payments.models import Payment
from remusgold.store.models import Item


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'user',
            'item',
            'quantity',
            'created_date',
        )

    def get(self, validated_data):
        id = validated_data.pop('id')
        payments = Payment.objects.filter(user_id=id)
        payment_list = []
        for payment in payments:
            item = Item.objects.get(id=payment.item_id)
            payment_list.append({'created_date': payment.created_date, 'item_id': item.id, 'item_name': item.name, 'item_image': item.images, 'quantity': payment.quantity})
        return payments

    def create(self, validated_data):
        quantity = validated_data.get('quantity')
        payment = Payment.objects.create(**validated_data)
        item = Item.objects.get(id=payment.item_id)
        return payment

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



