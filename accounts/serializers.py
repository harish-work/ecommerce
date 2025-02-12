from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import (User,
                     Category,
                     Product,
                     Orders,
                     Review,
                     ReturnOrders)
from django.contrib.auth import authenticate


class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ['email','name','phone','password']
        extra_kwargs = {"password":{"write_only":True}}

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

    def update(self,instance,validated_data):
        password = validated_data.pop('password',None)
        user = super().update(instance,validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    # def update(self,instance,validated_data):
    #     instance.name = validated_data.get('name',instance.name)
    #     instance.phone = validated_data.get('phone', instance.phone)
    #     instance.save()

    # def validate_phone(self,value):
    #     """filed level validation"""
    #     if len(value) < 8:
    #         raise serializers.ValidationError("phone number too short")
    #     return value

    # def validate(self,data):
    #     """object level validation"""
    #     if len(data['phone']) < 8:
    #         raise serializers.ValidationError("phone number too short")
    #     return data


class AuthTokenSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email,password=password)

        if not user:
            raise serializers.ValidationError("Invaid credentials")
        attrs['user'] = user
        return attrs


class ProductSerializer(ModelSerializer):
    category = serializers.CharField(source='category.type',read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializers(ModelSerializer):
    # products = ProductSerializer(many=True,read_only=True)
    # products = serializers.StringRelatedField(many=True)
    products = serializers.HyperlinkedRelatedField(many=True,
        read_only=True,
        view_name='createproducts-detail')

    class Meta:
        model = Category
        fields = '__all__'


class PlaceOrderSerializers(ModelSerializer):
    class Meta:
        model = Orders
        # fields = '__all__'
        exclude = ('product','user','return_status')

class ListOrderSerializers(ModelSerializer):
    user = serializers.CharField(source='user.name',read_only=True)
    user_address = serializers.CharField(source='user.adress',read_only=True)
    product = serializers.CharField(source='product.name',read_only=True)
    product_price = serializers.CharField(source='product.price', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = '__all__'
        # exclude = ('product',)
    def get_total_price(self,obj):
        return obj.quantity * obj.product.price

class ListReviewSerializers(ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class WriteReviewSerializers(ModelSerializer):
    class Meta:
        model = Review
        exclude = ('review_user','review_product')


class ListReturnSerializers(ModelSerializer):
    class Meta:
        model = ReturnOrders
        fields = '__all__'

class CreateReturnSerializers(ModelSerializer):
    class Meta:
        model = ReturnOrders
        # fields = '__all__'
        exclude = ('user', 'order','status','return_status')