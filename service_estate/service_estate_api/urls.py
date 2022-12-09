from django.urls import path
from service_estate_api import views
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, 'Product')
router.register('offerings', views.OfferingViewSet, 'Offering')
router.register('jobs', views.JobViewSet, 'Job')

urlpatterns = [
    path('', include(router.urls)),
    #path('jobs/', views.JobViewSet.as_view()),
    #path('products/', views.ProductView.as_view()),
    #path('products/<str:uuid>/', views.ProductDetailView.as_view()),
    #path('offerings/', views.OfferingView.as_view()),
    #path('offerings/<str:uuid>/', views.OfferingDetailView.as_view())
]