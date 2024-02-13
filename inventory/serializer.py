from rest_framework import serializers
from .models import Categories, Tags, Items, ItemTags 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('category_id', 'name')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('tag_id', 'name', 'imagelink')

class ItemTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    class Meta:
        model = ItemTags
        fields = ('item', 'tag')

class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = Items
        fields = ('item_id', 'sku', 'name', 'category', 'description', 'tags', 'in_stock_quantity', 'available_stock_quantity', 'low_stock_threshold')

    def create(self, validated_data):
        sku = validated_data.pop('sku')
        name = validated_data.pop('name')
        category = validated_data.pop('category')
        category = Categories.objects.get_or_create(name=category['name'])[0]
        description = validated_data.pop('description')
        tags = validated_data.pop('tags')
        in_stock_quantity = validated_data.pop('in_stock_quantity')
        available_stock_quantity = validated_data.pop('available_stock_quantity')
        low_stock_threshold = validated_data.pop('low_stock_threshold')
        item = Items.objects.create(sku=sku, name=name, category=category, description=description, in_stock_quantity=in_stock_quantity,
                                    available_stock_quantity=available_stock_quantity, low_stock_threshold=low_stock_threshold)
        for tag in tags:
            tag_id = Tags.objects.get(name=tag["name"])
            item.tags.add(tag_id)
        return item

