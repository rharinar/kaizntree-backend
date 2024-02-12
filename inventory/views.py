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


# class itemListView(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     # pagination_class = LimitOffsetPagination
#     def get(self, request, *args, **kwargs):
#         #Search
#         items = Items.objects.all()
#         search_query = request.query_params.get('search', None)
#         if search_query:
#             items = items.filter(name__icontains=search_query)
    
#         # Filter by category
#         category_id = request.query_params.get('category_id', None)
#         print(category_id)
#         if category_id:
#             items = items.filter(category_id=category_id)

#         # Sort
#         sort_by = request.query_params.get('sort_by', None)
#         if sort_by:
#             items = items.order_by(sort_by)

#         serializer = ItemSerializer(items, many=True)
#         return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def itemList(request):
    items = Items.objects.all()
    
    #Search
    search_query = request.query_params.get('search', None)
    if search_query:
        items = items.filter(name__icontains=search_query)
    
    # Filter by category
    category_id = request.query_params.get('category_id', None)
    print(category_id)
    if category_id:
        items = items.filter(category_id=category_id)

    # Sort
    sort_by = request.query_params.get('sort_by', None)
    if sort_by:
        items = items.order_by(sort_by)
    
    paginator = PageNumberPagination()
    paginator.page_size = 2
    result_page = paginator.paginate_queryset(items, request)
    serializer = ItemSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
    # serializer = ItemSerializer(items, many=True)
    # return Response(serializer.data)

@api_view(['POST'])
def create_item(request):
    print(request.data)
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# #create a user to display
# class UserListCreate(generics.ListCreateAPIView):
#     queryset = InventoryUser.objects.all()
#     serializer_class = UserSerializer

# #to retrieve, update or delete a user by ID
# class UserRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
#     queryset = InventoryUser.objects.all()
#     serializer_class = UserSerializer

# #create a category to display
# class CategoryListCreate(generics.ListCreateAPIView):
#     queryset = Categories.objects.all()
#     serializer_class = CategorySerializer

# #to retrieve, update or delete a category by ID
# class CategoryRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Categories.objects.all()
#     serializer_class = CategorySerializer

# #create a item to display
# class ItemListCreate(generics.ListCreateAPIView):
#     queryset = Items.objects.all()
#     serializer_class = ItemSerializer

# #to retrieve, update or delete a category by ID
# class ItemRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Items.objects.all()
#     serializer_class = ItemSerializer