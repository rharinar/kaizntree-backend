# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'categories'


class ItemTags(models.Model):
    item = models.OneToOneField('Items', models.DO_NOTHING, primary_key=True)  
    tag = models.ForeignKey('Tags', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'item_tags'
        unique_together = (('item', 'tag'),)

class Tags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    imagelink = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'

class Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    sku = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tags, through='ItemTags')
    in_stock_quantity = models.IntegerField()
    available_stock_quantity = models.IntegerField()
    low_stock_threshold = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'items'

