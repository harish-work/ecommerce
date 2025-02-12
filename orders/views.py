from django.shortcuts import render
from accounts.models import Orders,Product,User,ReturnOrders
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import generics
from accounts.serializers import (ListOrderSerializers,
                                  PlaceOrderSerializers,
                                  ListReturnSerializers,
                                  CreateReturnSerializers)
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status
# Create your views here.

class ListOrdersView(generics.ListAPIView):
    """List orders of authenticated users"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ListOrderSerializers

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user,return_status='not returned')


class PlaceOrderView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PlaceOrderSerializers
    # def get_queryset(self):
    #     return Orders.objects.all()
    def default_time(self):
        return timezone.now() + timezone.timedelta(+4)

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        product = Product.objects.get(pk=pk)
        if product.quantity >= serializer.validated_data['quantity']:
            product.quantity -= serializer.validated_data['quantity']
            product.save()
        else:
            raise ValidationError("Product Out off Stock !!")

        user = self.request.user
        serializer.validated_data['delivery_date'] = self.default_time()
        serializer.save(user=user,product=product)

class RetrieveOrderView(generics.RetrieveDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ListOrderSerializers
    # queryset = Orders.objects.all()

    def get_queryset(self):
        pk = self.kwargs['pk']
        # print(pk)
        # print(Orders.objects.filter(pk=pk,user=self.request.user))
        return Orders.objects.filter(pk=pk,user=self.request.user)


class ListReturnOrderView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | IsAdminUser]
    serializer_class = ListReturnSerializers
    # print(permission_classes == IsAuthenticated)
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ReturnOrders.objects.all()
        else:
            return ReturnOrders.objects.filter(user=self.request.user)


class CreateReturnOrderView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateReturnSerializers

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        user = self.request.user
        order = Orders.objects.get(pk=pk, user=user.id)
        if order:
            order.return_status = 'pending'
            order.save()
            return serializer.save(user=user,order=order)
        else:
            raise ValidationError("Please order the product first")


class UpdateReturnOrderView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ListReturnSerializers

    def get_object(self):
        pk = self.kwargs.get('pk')
        return ReturnOrders.objects.get(pk =pk)

    def perform_update(self, serializer):
        pk = self.kwargs.get('pk')
        return_order = ReturnOrders.objects.get(pk=pk)
        order_id = return_order.order.id
        if serializer.validated_data['status'] == True:
            order = Orders.objects.get(pk=order_id)
            order.return_status = 'returned'
            order.save()
            serializer.validated_data['return_status'] = 'returned'
        else:
            pass
        return serializer.save()





# class UpdateOrdersView(APIView):