from rest_framework import serializers
from .models import InventoryUser, Categories, Tags, StockStatus, Items, ItemTags 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryUser
        fields = ('id', 'name', 'gender', 'age')

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
        fields = ('item_id', 'sku', 'name', 'category', 'description', 'tags')

    def create(self, validated_data):
        sku = validated_data.pop('sku')
        name = validated_data.pop('name')
        category = validated_data.pop('category')
        category = Categories.objects.get_or_create(name=category['name'])[0]
        description = validated_data.pop('description')
        tags = validated_data.pop('tags')
        item = Items.objects.create(sku=sku, name=name, category=category, description=description)
        for tag in tags:
            tag_id = Tags.objects.get(name=tag["name"])
            item.tags.add(tag_id)
        return item

