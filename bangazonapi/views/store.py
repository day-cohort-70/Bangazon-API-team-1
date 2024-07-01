from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from bangazonapi.models import Store, Customer


class StoreSerializer(serializers.ModelSerializer):
    """JSON serializer for stores"""

    class Meta:
        model = Store
        fields = ('name', 'description', 'seller',)
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
