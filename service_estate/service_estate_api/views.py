from django.shortcuts import render
from service_estate_api import models, serializers
from service_estate_api.permissions import IsOwnerOrReadOnly
from rest_framework import status, viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from service_estate_api.filters import ProductFilter, OfferingFilter
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.renderers import AdminRenderer
import uuid, datetime
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    #filterset_fields = ['name', 'status']
    #ordering_fields = ['name']
    filter_class = ProductFilter 
    #renderer_classes = ['AdminRenderer']
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    #def get_queryset(self):
    #    queryset = models.Product.objects.all()
        

    #def perform_create(self, serializers):
    #    serializers.save(owner=self.request.user)



class OfferingViewSet(viewsets.ModelViewSet):
    queryset = models.Offering.objects.all()
    serializer_class = serializers.OfferingSerializer
    #filterset_fields = ['name', 'status']
    filter_class = OfferingFilter

class ProductView(APIView):
    def get(self, request, format=None):
        products = models.Product.objects.all()
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductDetailView(APIView):
    def get(self, request, uuid, format=None):
        product = models.Product.objects.get(pk=uuid)
        serializer = serializers.ProductSerializer(product)
        return Response(serializer.data)

    def delete(self, request, uuid, format=None):
        product = models.Product.objects.get(pk=uuid)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, uuid, format=None):
        product = models.Product.objects.get(pk=uuid)
        serializer = serializers.ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OfferingView(APIView):

    def get(self, request, format=None):
        offering = models.Offering.objects.all()
        serializer = serializers.OfferingSerializer(offering, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.OfferingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OfferingDetailView(APIView):
    def get(self, request, uuid, format=None):
        offering = models.Offering.objects.get(pk=uuid)
        serializer = serializers.OfferingSerializer(offering)
        return Response(serializer.data)

    def delete(self, request, uuid, format=None):
        offering = models.Offering.objects.get(pk=uuid)
        offering.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, uuid, format=None):
        offering = models.Offering.objects.get(pk=uuid)
        serializer = serializers.OfferingSerializer(offering, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobViewSet(viewsets.ModelViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer

    @action(detail=True, methods=['get'], url_path='detail')
    def job_detail(self, request, pk=None):
        queryset = self.get_object()
        serializer = serializers.JobDetailSerializer(queryset)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='launch_job')
    def launch_job(self, request):
        data = request.data
        data["triger_at"] = datetime.datetime.now(datetime.timezone.utc)
        data["execution_id"] = str(uuid.uuid4())

        serializer = serializers.JobSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def launch_job(request):
    data = request.data
    data["triger_at"] = datetime.datetime.now(datetime.timezone.utc)
    data["execution_id"] = uuid.uuid4()
    serializer = serializers.JobSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    