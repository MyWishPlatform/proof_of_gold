from rest_framework import serializers
from remusgold.account.models import AdvUser, BillingAddress, ShippingAddress
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password, ValidationError, MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator, UserAttributeSimilarityValidator

class PatchSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField()
    class Meta:
        model = AdvUser
        fields= ('username', 'email', 'first_name', 'last_name', 'password', 'new_password')

    def update(self, instance, validated_data):
        print('here', flush= True)
        try:
            if validated_data['password']:
                print('here1', flush=True)
                password = validated_data.pop('password')
                check = instance.check_password(password)
                print(check, flush= True)
                if check:
                    print('here2', flush=True)
                    new_password = validated_data.pop('new_password')
                    try:
                        validate_password(new_password, user=instance, password_validators= [MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator, UserAttributeSimilarityValidator])
                    except ValidationError:
                        return 'Password validation error'
                    hashed_password = make_password(new_password, salt=None, hasher='default')
                    setattr(instance, 'password', hashed_password)
        except KeyError as e:
            print(e)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class PatchShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PatchBillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = '__all__'

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance