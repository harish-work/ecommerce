from django.urls import path
from .views import (ListOrdersView,
                    PlaceOrderView,
                    RetrieveOrderView,
                    ListReturnOrderView,
                    CreateReturnOrderView,
                    UpdateReturnOrderView,)
urlpatterns = [
    path('List_order/', ListOrdersView.as_view(),name='list-orders'),
    path('product/<int:pk>/place_order/', PlaceOrderView.as_view(),name='place-orders'),
    path('fetch_orders/<int:pk>/', RetrieveOrderView.as_view(),name='fetch-orders'),
    path('list_return_orders/', ListReturnOrderView.as_view(),name='list-return'),
    path('fetch_orders/<int:pk>/place_return/', CreateReturnOrderView.as_view(),name='place-return'),
    path('fetch_retrun_orders/<int:pk>/update_return/', UpdateReturnOrderView.as_view(),name='update-return'),

]