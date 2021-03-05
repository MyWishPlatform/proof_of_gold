from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from remusgold.account.models import AdvUser, BillingAddress, ShippingAddress
from remusgold.settings import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_PASSWORD


class PatchSerializer(serializers.ModelSerializer):
    '''
    Serialiser for AdvUser model patching
    '''
    new_password = serializers.CharField()
    class Meta:
        model = AdvUser
        fields= ('username', 'email', 'first_name', 'last_name', 'password', 'new_password')

    def update(self, instance, validated_data):
        print('here', flush= True)
        print('started patch')
        try:
            if validated_data['new_password']:
                new_password = validated_data.pop('new_password')
                hashed_password = make_password(new_password, salt=None, hasher='default')
                setattr(instance, 'password', hashed_password)
        except KeyError:
            pass
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



class PatchShippingAddressSerializer(serializers.ModelSerializer):
    '''
    Serialiser for ShippingAddress model patching
    '''
    class Meta:
        model = ShippingAddress
        fields = '__all__'

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value != '':
                setattr(instance, attr, value)
        instance.save()
        return instance


class PatchBillingAddressSerializer(serializers.ModelSerializer):
    '''
    Serialiser for BillingAddress model patching
    '''
    class Meta:
        model = BillingAddress
        fields = '__all__'

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value !=	'':
                setattr(instance, attr, value)
        instance.save()
        return instance



