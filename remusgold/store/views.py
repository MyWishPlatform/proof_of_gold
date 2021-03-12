from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from remusgold.store.models import Item, Group, Review
from remusgold.settings import ALLOWED_HOSTS
from remusgold.account.models import get_mail_connection
from remusgold.templates.email.contact_us_body import contact_us_body, contact_us_style
from django.core.mail import send_mail
from remusgold.settings import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_PASSWORD

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
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'bonus_coins': openapi.Schema(type=openapi.TYPE_NUMBER),
            'lucky_prize': openapi.Schema(type=openapi.TYPE_NUMBER)
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
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'bonus_coins': openapi.Schema(type=openapi.TYPE_NUMBER),
            'lucky_prize': openapi.Schema(type=openapi.TYPE_NUMBER)
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
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'bonus_coins': openapi.Schema(type=openapi.TYPE_NUMBER),
            'lucky_prize': openapi.Schema(type=openapi.TYPE_NUMBER)
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

search_response = openapi.Response(
    description='Response with search results',
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'group': openapi.Schema(type=openapi.TYPE_STRING),
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'image': openapi.Schema(type=openapi.TYPE_OBJECT),
            'total_supply': openapi.Schema(type=openapi.TYPE_NUMBER),
            'supply': openapi.Schema(type=openapi.TYPE_NUMBER),
            'sold': openapi.Schema(type=openapi.TYPE_NUMBER),
            'price': openapi.Schema(type=openapi.TYPE_NUMBER),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'bonus_coins': openapi.Schema(type=openapi.TYPE_NUMBER),
            'lucky_prize': openapi.Schema(type=openapi.TYPE_NUMBER)
        },
    ))
)
class GroupView(APIView):
    '''
    get all items in category
    '''
    @swagger_auto_schema(
        operation_description="get all items by group",
        responses={200: group_response},
    )
    def get(self, request, group):
        item_list = []
        group_object = Group.objects.get(name=group)
        items = Item.objects.filter(group_id=group_object.id)

        for item in items:
            reviews = Review.objects.filter(item=item)
            review_list = []
            for review in reviews:
                if review.active:
                    review_list.append(
                        {'rate': review.rate, 'body': review.body, 'name': review.name, 'email': review.email,
                         'created_at': review.created_date.strftime("%m/%d/%Y, %H:%M:%S")})
            item_list.append({'id': item.id, 'group': item.group.name, 'name': item.name,
                              'image': ALLOWED_HOSTS[0] + item.images.url,
                              'total_supply': item.total_supply, 'supply': item.supply, 'reserved': item.reserved,
                              'sold': item.sold, 'price': item.price, 'description': item.description,
                              'bonus_coins': item.ducatus_bonus, 'lucky_prize':item.lucky_prize, 'reviews': review_list})
        response_data = {
            'items': item_list,
        }
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)

class StoreView(APIView):
    '''
    get all existing items
    '''
    @swagger_auto_schema(
        operation_description="get all items",
        responses={200: store_response},
    )

    def get(self, request):
        item_list = []
        items = Item.objects.all()
        for item in items:
            reviews = Review.objects.filter(item=item)
            review_list = []
            for review in reviews:
                if review.active:
                    review_list.append(
                        {'rate': review.rate, 'body': review.body, 'name': review.name, 'email': review.email,
                         'created_at': review.created_date.strftime("%m/%d/%Y, %H:%M:%S")})
            item_list.append({'id': item.id, 'group': item.group.name, 'name': item.name, 'image': ALLOWED_HOSTS[0] + item.images.url,
                    'total_supply': item.total_supply, 'supply': item.supply, 'reserved': item.reserved, 'sold': item.sold,
                    'price': item.price, 'description': item.description, 'bonus_coins': item.ducatus_bonus,
                    'lucky_prize': item.lucky_prize, 'reviews': review_list})
        response_data = {
            'items': item_list,
        }
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)


class UniqueView(APIView):
    '''
    get single item.
    Maybe is deprecated due to frontend not using it (check).
    '''
    @swagger_auto_schema(
        operation_description="get single item",
        responses={200: unique_response},
    )
    def get(self, request, id):
        item = Item.objects.get(id=id)
        reviews = Review.objects.filter(item=item)
        review_list = []
        for review in reviews:
            if review.active:
                review_list.append({'rate': review.rate, 'body': review.body, 'name': review.name, 'email': review.email,
                                    'created_at': review.created_date.strftime("%m/%d/%Y, %H:%M:%S")})
        res_item = {'id': item.id, 'group': item.group.name, 'name': item.name,
                'total_supply': item.total_supply, 'supply': item.supply, 'reserved': item.reserved, 'image': ALLOWED_HOSTS[0] + item.images.url,
                'sold': item.sold, 'price':item.price, 'description': item.description, 'bonus_coins': item.ducatus_bonus,
                'lucky_prize': item.lucky_prize, 'reviews': review_list}
        response_data = res_item
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)

      
@method_decorator(csrf_exempt, name='dispatch')
class ReviewView(APIView):
    '''
    View for posting review. get is included in item views
    '''
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
        review = Review(item_id=item_id, rate=rate, body=body, name=name, email=email)
        review.save()
        response_data = {'id': review.id, 'item_id': review.item_id, 'rate': review.rate, 'body': review.body,
                         'name': review.name, 'email': review.email, 'created_at': review.created_date}

        return Response(response_data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class SearchView(APIView):
    '''
    View for search items in shop.
    searching has simple 'contains' logic.
    '''
    @swagger_auto_schema(
        operation_description="post search pattern",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'text': openapi.Schema(type=openapi.TYPE_STRING)}),
        responses={200: search_response},
)

    def post(self, request):
        print(request)
        request_data = request.data
        print(request_data)
        words = request_data.get('text')
        words = words.split(' ')
        items = Item.objects.all()
        for word in words:
            items = items.filter(name__icontains=word)
        print(items.__dict__)
        search_result = []
        for item in items:
            reviews = Review.objects.filter(item=item)
            review_list = []
            for review in reviews:
                if review.active:
                    review_list.append(
                        {'rate': review.rate, 'body': review.body, 'name': review.name, 'email': review.email,
                         'created_at': review.created_date.strftime("%m/%d/%Y, %H:%M:%S")})
            search_result.append({'id': item.id, 'group': item.group.name, 'name': item.name, 'image': ALLOWED_HOSTS[0] + item.images.url,
                    'total_supply': item.total_supply, 'supply': item.supply, 'reserved': item.reserved, 'sold': item.sold, 'price': item.price,
                    'description': item.description, 'bonus_coins': item.ducatus_bonus, 'lucky_prize':item.lucky_prize, 'reviews': review_list})
        return Response(search_result, status=status.HTTP_200_OK)



@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['api_key', 'data']
    ),
)


@api_view(http_method_names=['POST'])
def contact_us(request):
    '''
    view for contact us form, which sends message to shop's email.
    Placed in store because I didn't found better place.
    '''
    request_data = request.data
    name = request_data.get('name')
    email = request_data.get('email')
    message = request_data.get('message')

    connection = get_mail_connection()
    html_body = contact_us_body.format(user=name, email=email, message=message)

    send_mail(
        'contact_us_form',
        '',
        EMAIL_HOST_USER,
        ['INFO@D-POG.com'],
        connection=connection,
        html_message=contact_us_style + html_body,
    )
    print('message sent')
    return Response('OK', status=status.HTTP_200_OK)