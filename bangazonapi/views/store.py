from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from bangazonapi.models import Store, Customer


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "url",)
        depth = 1

class SellerSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Customer
        fields = (
            "url", "phone_number", "address", "user",)
        depth = 1

class StoreSerializer(serializers.ModelSerializer):
    """JSON serializer for stores"""
    seller = SellerSerializer(many=False)

    class Meta:
        model = Store
        fields = ('id', 'name', 'description', 'seller')
        depth = 1
        


class Stores(ViewSet):
    """Request handlers for seller store info in the Bangazon Platform"""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        """
        @api {GET} /stores GET all stores
        @apiName GetStores
        @apiGroup Stores

        @apiHeader {string} Authorization Auth Token
        @apiHeaderExample {string} Authorization Token 9ba45f09651c5b0c404f37a2d2572c026c14669c

        @apiSuccess (200) {Object[]} stores Array of store objects
        @apiSuccessExample {json} Success
            [
                {
                    "name": "The Hungry Hippo",
                    "description": "A quirky store that sells used toys!",
                    "seller": {
                        "id": 4,
                        "phone_number": "555-1212",
                        "address": "100 Infinity Way",
                        "user": 5
                    }
                }
            ]
        """
        try:
            stores = Store.objects.all()
            serializer = StoreSerializer(stores, many=True, context={"request": request})
            return Response(serializer.data)
        
        except Store.DoesNotExist as ex:
            return Response({'message': 'There are no stores'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """
        Creates a new store.
        """
        # Extract data from the request
        name = request.data.get('name')
        description = request.data.get('description')

        # Check if the customer already exists
        current_user = Customer.objects.get(user=request.auth.user)

        try:
            store = Store.objects.get(seller=current_user)
            print(store.id)
        except Customer.DoesNotExist:
            # If the store does not exist, create one
            store = Store.objects.create(name=name, description=description, seller=current_user)        

        # Return the created store
        serializer = StoreSerializer(store, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        try:
            store = Store.objects.get(pk=pk)
            serializer = StoreSerializer(store, context={"request": request})
            return Response(serializer.data)

        except store.DoesNotExist :
            return Response(
                {
                    "message": "The requested store does not exist, or you do not have permission to access it."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as ex:
            return HttpResponseServerError(ex)