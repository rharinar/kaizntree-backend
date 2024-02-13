import json
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, mixins, status
from .models import Categories, Items
from .serializer import CategorySerializer, ItemSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from django.contrib.postgres.search import SearchQuery, SearchVector
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# from django.utils.hashing import md5
import hashlib


def generate_cache_key(request):
    # Create a unique cache key based on the request's query parameters
    params = sorted(request.query_params.items())
    key = hashlib.md5(json.dumps(params).encode('utf-8')).hexdigest()
    return f'items_{key}'

item_response_example = [{
    "item_id": 1,
    "sku": "12345ABC",
    "name": "Sample Item",
    "category": {
        "category_id": 1,
        "name": "Sample Category"
    },
    "description": "This is a sample item description.",
    "tags": [],
    "in_stock_quantity": 100,
    "available_stock_quantity": 90,
    "low_stock_threshold": 10
}]

@swagger_auto_schema(
    method='get',
    operation_description="Lists all items, with optional filtering by search query, category, and sorting.",
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search term for item name or description", type=openapi.TYPE_STRING),
        openapi.Parameter('category_id', openapi.IN_QUERY, description="Category ID to filter items", type=openapi.TYPE_INTEGER),
        openapi.Parameter('sort_by', openapi.IN_QUERY, description="Field name to sort items", type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response(
            description="A list of items.",
            schema=ItemSerializer(many=True),
            examples={
                'application/json': item_response_example
            }
        )
    },
    security=[{'Bearer': []}],
)
# Define a view to list items
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def item_list(request):
    """
    Retrieves a list of items with optional search, filtering, and sorting.
    - `search`: Query items by name or description.
    - `category_id`: Filter items by category.
    - `sort_by`: Sort items by a specified field.
    """
    try:
        # Check if items are cached, retrieve them if available, otherwise query the database
        cache_key = generate_cache_key(request)
        cached_items = cache.get(cache_key)
        if cached_items:
            return Response(cached_items)
        else:
            items = Items.objects.all()
        # if cache.get('items'):
        #     items = cache.get('items')
        # else:
        #     items = Items.objects.all()
        #     cache.set('items', items, timeout=10)

        # Search functionality
        search_query = request.query_params.get('search', None)
        if search_query:
            vector = (SearchVector("sku")+SearchVector("name")+SearchVector("description"))
            items = items.annotate(search=vector).filter(search__icontains=search_query).order_by("name")
        
        # Filter by category
        category_id = request.query_params.get('category_id', None)
        if category_id:
            items = items.filter(category_id=category_id)

        # Sort functionality
        sort_by = request.query_params.get('sort_by', None)
        if sort_by:
            items = items.order_by(sort_by)
        
        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 2
        page_size = request.query_params.get('page_size', None)
        if page_size:
            paginator.page_size = page_size
        result_page = paginator.paginate_queryset(items, request)
        serializer = ItemSerializer(result_page, many=True)
        cache.set(cache_key, serializer.data, timeout=10)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@swagger_auto_schema(
    method='post', 
    operation_description="Create a new item.",
    request_body=ItemSerializer,
    responses={201: ItemSerializer, 400: 'Bad Request'}
)
# Define a view to create an item
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    """
    Creates a new item with the provided details.
    """
    try:
        # Deserialize the incoming data and validate it
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            # Save the valid data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@swagger_auto_schema(
    method='post', 
    operation_description="Create a new category.",
    request_body=CategorySerializer,
    responses={201: CategorySerializer, 400: 'Bad Request'}
)
# Define a view to create a category
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    """
    Creates a new category.
    """
    try:
        # Deserialize the incoming data and validate it
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            # Save the valid data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
