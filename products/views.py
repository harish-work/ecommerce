from django.shortcuts import render
from accounts.models import (Category,
                            Product,
                            Review,
                             Orders)
from accounts.serializers import (CategorySerializers,
                                  ProductSerializer,
                                  ListReviewSerializers,
                                  WriteReviewSerializers)
from .task import my_task
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from .pagination import ProductPagination
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from rest_framework.views import APIView
# Create your views here.

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class ProductCreateView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    pagination_class = ProductPagination
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price']
    # parser_classes = [MultiPartParser,FileUploadParser]


# class ListReviewView(generics.ListAPIView):
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAuthenticated]
#     queryset = Review.objects.all()
#     serializer_class = ListReviewSerializers

class WriteReviewView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = WriteReviewSerializers

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        user = self.request.user
        order = Orders.objects.get(pk =pk ,user=user.id)
        if order:
            product_id = order.product
            products = Product.objects.get(pk=product_id.id)
            review = Review.objects.filter(review_product=product_id)
            # print(len(review)+1)
            # print(serializer.validated_data['rating'])
            # print(products.avg_rating)
            # print(products.avg_rating + serializer.validated_data['rating'])
            products.avg_rating =  (products.avg_rating + serializer.validated_data['rating']) / (len(review) + 1)
            products.save()

        else:
            raise ValidationError("review allowed after the purchase")
        serializer.save(review_user=user,review_product=products)


class TestTaskView(APIView):
    def post(self,request):
        a = request.data['a']
        b = request.data['b']
        result  = my_task.delay(a,b)
        return Response({"data":"done"},status=status.HTTP_200_OK)


class OrmView(APIView):
    def get(self,request):
        order = Orders.objects.get(id=2)
        # order = Orders.objects.select_related('product').get(id=2)
        print(order.product.description)