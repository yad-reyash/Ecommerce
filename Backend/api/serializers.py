from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField()
    image = serializers.CharField()
    colors = serializers.ListField(child=serializers.CharField())
    sizes = serializers.ListField(child=serializers.IntegerField())
    category = serializers.CharField()
    brand = serializers.CharField()
    featured = serializers.BooleanField()


class CartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    size = serializers.IntegerField(allow_null=True)
    color = serializers.CharField(allow_null=True)
    image = serializers.CharField()


class ScrapeRequestSerializer(serializers.Serializer):
    url = serializers.URLField()


class SearchRequestSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=200)
    site = serializers.ChoiceField(
        choices=['nike', 'adidas', 'amazon', 'all'],
        default='all'
    )


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    message = serializers.CharField()


class ScrapedProductSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True)
    price = serializers.CharField(allow_null=True)
    image = serializers.CharField(allow_null=True)
    link = serializers.CharField(allow_null=True)
    brand = serializers.CharField(allow_null=True, required=False)
    rating = serializers.CharField(allow_null=True, required=False)