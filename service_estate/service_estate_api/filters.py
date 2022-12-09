import rest_framework_filters as filters
from service_estate_api.models import Product, Offering


class ProductFilter(filters.FilterSet):
    offering = filters.RelatedFilter("service_estate_api.filters.OfferingFilter", field_name="offering", 
                                     queryset=Offering.objects.all(), label="Offering")
    status = filters.CharFilter("status", label="Status")
    name = filters.CharFilter("name", label="Name")

    def is_status_active(self, ps, name, value):
        return ps.filter(**{
            name: value,
        })

class OfferingFilter(filters.FilterSet):
    #product = filters.RelatedFilter(ProductFilter, field_name="name", queryset=Product.objects.all())
    #product= filters.ModelChoiceFilter(queryset=Product.objects.all())
    #product_name = filters.RelatedFilter(filterset=ProductFilter, field_name='name',
    # label='product_name', lookup_expr='exact', queryset=Product.objects.all())
    name = filters.CharFilter("name", label="Name")
    product = filters.RelatedFilter("service_estate_api.filters.ProductFilter", field_name="product", queryset=Product.objects.all(), label="Product")


