from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (CategoryView,
                    ProductCreateView,
                    WriteReviewView,
                    TestTaskView,
                    OrmView)
router = DefaultRouter()
router.register('category',CategoryView,basename='category')
router.register('products',ProductCreateView,basename='createproducts')
urlpatterns = [
    path('', include(router.urls)),
    path('fetch_orders/<int:pk>/write_review/', WriteReviewView.as_view(),name='write-review'),
    path('celery_test/',TestTaskView.as_view()),
    path('test/', OrmView.as_view())

]