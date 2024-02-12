from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, mixins, status
from .models import InventoryUser, Categories, Items
from .serializer import UserSerializer, CategorySerializer, ItemSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache

# Define a view to list items
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def item_list(request):
    try:
        # Check if items are cached, retrieve them if available, otherwise query the database
        items = Items.objects.all()
        # if cache.get('items'):
        #     items = cache.get('items')
        # else:
        #     items = Items.objects.all()
        #     cache.set('items', items, timeout=10)

        # Search functionality
        search_query = request.query_params.get('search', None)
        if search_query:
            items = items.filter(name__icontains=search_query)
        
        # Filter by category
        category_id = request.query_params.get('category_id', None)
        print(category_id)
        if category_id:
            items = items.filter(category_id=category_id)

        # Sort functionality
        sort_by = request.query_params.get('sort_by', None)
        if sort_by:
            items = items.order_by(sort_by)
        
        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 2
        result_page = paginator.paginate_queryset(items, request)
        serializer = ItemSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Define a view to create an item
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
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

# Define a view to create a category
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
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
