from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from oscar.apps.basket.views import BasketView as BasketViewCore
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import BasketSerializer, BasketLinePatchSerializer, BasketCheckParamsSerializer
from .models import Basket, Line
from application.catalogue.models import Product
from application.partner.models import StockRecord


class BasketView(BasketViewCore):
    def json_response(self, ctx, flash_messages):
        basket_html = render_to_string(
            'oscar/basket/partials/basket_content.html',
            context=ctx, request=self.request)

        mini_basket_html = render_to_string(
            'oscar/partials/mini_basket.html',
            context=ctx, request=self.request)

        return JsonResponse({
            'content_html': basket_html,
            'messages': flash_messages.as_dict(),
            'mini_basket_html': mini_basket_html,
        })


class BaseBasketView(APIView):
    def get_object(self):
        # If neither basket nor basket_id exist, create basket in DB and record basket ID to the session.
        # todo: take into account status submitted. If submitted create new basket.
        # todo: delete line if product not browsable or not exist.
        try:
            # todo: prefetch products
            basket = Basket.objects.get(pk=self.request.session['basket_id'])
        except (Basket.DoesNotExist, KeyError):
            basket = Basket.objects.create()
            self.request.session['basket_id'] = basket.id
        basket.strategy = self.request.strategy
        # See middleware
        # self.apply_offers_to_basket(request, basket)
        return basket
        # return self.request.basket


class BasketAPIView(BaseBasketView):

    def get(self, request, *args):
        basket = self.get_object()
        serializer = BasketSerializer(basket, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        check_params_serializer = BasketCheckParamsSerializer(data=request.data)
        if not check_params_serializer.is_valid():
            return Response(check_params_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        basket = self.get_object()

        try:
            product = Product.objects.filter(structure='child').get(pk=request.data['sizeId'])
            stock_record = product.stockrecords.all()[:1].get()
        except (Product.DoesNotExist, StockRecord.DoesNotExist) as err:
            return Response(err.__str__(), status=status.HTTP_400_BAD_REQUEST)

        try:
            # If line exists initialize serializer to update it
            line = Line.objects.filter(basket=basket, product=product).get()
            line_serializer = BasketLinePatchSerializer(line, data=request.data)
            response_http_status = status.HTTP_200_OK
        except Line.DoesNotExist:
            # if line does not exist initialize serializer to create it
            line_serializer = BasketLinePatchSerializer(data=request.data)
            response_http_status = status.HTTP_201_CREATED

        if line_serializer.is_valid():
            line_instance = line_serializer.save(
                product=product,
                basket=basket,
                stock_record=stock_record,
            )
            if line_instance.quantity == 0:
                line_instance.delete()

        basket_updated = self.get_object()
        basket_serializer = BasketSerializer(basket_updated, context={'request': request})
        return Response(basket_serializer.data, status=response_http_status)

    def put(self, request):
        return self.patch(request)


class BasketDeleteAPIView(BaseBasketView):

    def delete(self, request, pk):
        product_id = pk
        if product_id is None:
            return Response({'product_id': ['This field is required']}, status=status.HTTP_400_BAD_REQUEST)

        basket = self.get_object()

        try:
            product = Product.objects.get(pk=product_id)
        except (Product.DoesNotExist, StockRecord.DoesNotExist) as err:
            # If product does not exist just return response with basket.
            basket_serializer = BasketSerializer(basket, context={'request': request})
            return Response(basket_serializer.data, status=status.HTTP_200_OK)

        try:
            # If line exists initialize serializer to update it
            line = Line.objects.filter(basket=basket, product=product).get()
            line.delete()
            response_http_status = status.HTTP_200_OK
        except Line.DoesNotExist:
            response_http_status = status.HTTP_200_OK

        basket_updated = self.get_object()
        basket_serializer = BasketSerializer(basket_updated, context={'request': request})
        return Response(basket_serializer.data, status=response_http_status)
