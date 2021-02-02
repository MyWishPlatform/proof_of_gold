from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.decorators import api_view

from remusgold.store.models import Item, Group, Review
from remusgold.settings import ALLOWED_HOSTS

group_response = openapi.Response(
    description='Response with all items in category',
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_OBJECT,
        properties={'items': openapi.Schema(type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'group': openapi.Schema(type=openapi.TYPE_STRING),
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'images': openapi.Schema(type=openapi.TYPE_OBJECT),
            'total_supply': openapi.Schema(type=openapi.TYPE_NUMBER),
            'supply': openapi.Schema(type=openapi.TYPE_NUMBER),
            'sold': openapi.Schema(type=openapi.TYPE_NUMBER),
            'price': openapi.Schema(type=openapi.TYPE_NUMBER),
                   },
        ), },
    ), )
)

store_response = openapi.Response(
    description='Response with all items',
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_OBJECT,
        properties={'items': openapi.Schema(type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'group': openapi.Schema(type=openapi.TYPE_STRING),
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'image': openapi.Schema(type=openapi.TYPE_OBJECT),
            'total_supply': openapi.Schema(type=openapi.TYPE_NUMBER),
            'supply': openapi.Schema(type=openapi.TYPE_NUMBER),
            'sold': openapi.Schema(type=openapi.TYPE_NUMBER),
            'price': openapi.Schema(type=openapi.TYPE_NUMBER),
        },
    ), }, ), )
)

unique_response = openapi.Response(
    description='Response with single item',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'group': openapi.Schema(type=openapi.TYPE_STRING),
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'image': openapi.Schema(type=openapi.TYPE_OBJECT),
            'total_supply': openapi.Schema(type=openapi.TYPE_NUMBER),
            'supply': openapi.Schema(type=openapi.TYPE_NUMBER),
            'sold': openapi.Schema(type=openapi.TYPE_NUMBER),
            'price': openapi.Schema(type=openapi.TYPE_NUMBER),
        },
    )
)

review_response = openapi.Response(
    description='Response with created review',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'item_id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'rate': openapi.Schema(type=openapi.TYPE_NUMBER),
            'body': openapi.Schema(type=openapi.TYPE_STRING),
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'created_at': openapi.Schema(type=openapi.TYPE_STRING),
        },
    )
)

class GroupView(APIView):

    @swagger_auto_schema(
        operation_description="get all items by group",
        responses={200: group_response},
    )
    def get(self, request, group):
        item_list = []
        group_object = Group.objects.get(name=group)
        items = Item.objects.filter(group_id=group_object.id)

        for item in items:
            item_list.append({'id': item.id, 'group': item.group.name, 'name': item.name, 'image': ALLOWED_HOSTS[0] + item.images.url,
                'total_supply':item.total_supply, 'supply': item.supply, 'sold': item.sold, 'price':item.price})
        response_data = {
            'items': item_list,
        }
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)

class StoreView(APIView):

    @swagger_auto_schema(
        operation_description="get all items",
        responses={200: store_response},
    )

    def get(self, request):
        item_list = []
        items = Item.objects.all()
        for item in items:
            item_list.append({'id': item.id, 'group': item.group.name, 'name': item.name, 'image': ALLOWED_HOSTS[0] + item.images.url,
                    'total_supply': item.total_supply, 'supply': item.supply, 'sold': item.sold, 'price': item.price})
        response_data = {
            'items': item_list,
        }
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)


class UniqueView(APIView):

    @swagger_auto_schema(
        operation_description="get single item",
        responses={200: unique_response},
    )
    def get(self, request, id):
        item = Item.objects.get(id=id)
        reviews = Review.objects.filter(item=item)
        review_list = []
        for review in reviews:
            review_list.append({'rate': review.rate, 'body': review.body, 'name':review.name, 'email': review.email,
                                'created_at': review.created_date.strftime("%m/%d/%Y, %H:%M:%S")})
        res_item= {'id': item.id, 'group': item.group.name, 'name': item.name,
                'total_supply':item.total_supply, 'supply': item.supply, 'image': ALLOWED_HOSTS[0] + item.images.url,
                'sold': item.sold, 'price':item.price, 'description': item.description, 'reviews': review_list}
        response_data =res_item
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)


class ReviewView(APIView):

    @swagger_auto_schema(
        operation_description="post review",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                        'item_id': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'rate': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'body': openapi.Schema(type=openapi.TYPE_STRING),
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                                }
                                ),
        responses={200: review_response},
    )
    def post(self, request):
        print(request)
        request_data = request.data
        print(request_data)
        item_id = request_data.get('item_id')
        rate = request_data.get('rate')
        body = request_data.get('body')
        name = request_data.get('name')
        email = request_data.get('email')
        review = Review(item_id=item_id, rate=rate, body=body, name=name, email = email)
        review.save()
        response_data = {'id': review.id, 'item_id': review.item_id, 'rate': review.rate, 'body': review.body,
                         'name': review.name, 'email': review.email, 'created_at': review.created_date}

        return Response(response_data, status=status.HTTP_200_OK)