from rest_framework import serializers
from service_estate_api.models import Product, Offering, Job

class ProductNameValidator(object):
    def __init__(self, number=3):
        self.number = number

    def __call__(self, value):
        if len(value) < self.number:
            message = 'This field must be more than %d charactors.' % self.number
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        pass

class ProductSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {'name': {'validators': [ProductNameValidator()]}}

class OfferingSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Offering
        fields = "__all__"

class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        depth = 2

class JobSerializer(serializers.ModelSerializer):
    execution_id = serializers.CharField(read_only=True)
    triger_at = serializers.DateTimeField(read_only=True)
    class  Meta:
        model = Job
        fields = "__all__"
        #fields = ("id","product", "workflow_name", "requester", "job_status")