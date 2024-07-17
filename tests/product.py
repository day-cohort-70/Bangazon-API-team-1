import json
import datetime
from rest_framework import status
from rest_framework.test import APITestCase


class ProductTests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
        }
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = "/productcategories"
        data = {"name": "Sporting Goods"}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "Sporting Goods")

    def create_product(self, name, price, quantity, description):
        """
        Helper method to create a product.
        """
        url = "/products"
        data = {
            "name": name,
            "price": price,
            "quantity": quantity,
            "description": description,
            "category_id": 1,
            "location": "Pittsburgh",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return json_response

    def test_create_product(self):
        """
        Ensure we can create a new product.
        """
        product = self.create_product("Kite", 14.99, 60, "It flies high")
        self.assertEqual(product["id"], 1)
        self.assertEqual(product["name"], "Kite")
        self.assertEqual(product["price"], 14.99)
        self.assertEqual(product["quantity"], 60)
        self.assertEqual(product["description"], "It flies high")
        self.assertEqual(product["location"], "Pittsburgh")

    def test_update_product(self):
        """
        Ensure we can update a product.
        """
        self.test_create_product()

        url = "/products/1"
        data = {
            "name": "Kite",
            "price": 24.99,
            "quantity": 40,
            "description": "It flies very high",
            "category_id": 1,
            "created_date": datetime.date.today(),
            "location": "Pittsburgh",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], "Kite")
        self.assertEqual(json_response["price"], 24.99)
        self.assertEqual(json_response["quantity"], 40)
        self.assertEqual(json_response["description"], "It flies very high")
        self.assertEqual(json_response["location"], "Pittsburgh")

    def test_get_all_products(self):
        """
        Ensure we can get a collection of products.
        """
        self.create_product("Kite", 14.99, 60, "It flies high")
        self.create_product("Umbrella", 19.99, 40, "It provides shade")
        self.create_product("Basketball", 24.99, 30, "It's for playing basketball")

        url = "/products"

        response = self.client.get(url, None, format="json")
        json_response = json.loads(response.content)
        print("Products list:", json_response)  # Debug print

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming the response is still nested by category
        products = json_response["products_by_category"].get("Sporting Goods", [])
        self.assertEqual(len(products), 3)

    def test_delete_product(self):
        """
        Ensure we can delete a product.
        """
        # First, create a product to delete
        product = self.create_product("Kite", 14.99, 60, "It flies high")
        product_id = product["id"]

        # Verify the product was created
        url = "/products"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get(url, format="json")
        json_response = json.loads(response.content)
        print("Products list after creation:", json_response)

        # Ensure the product with ID 1 exists
        products = json_response["products_by_category"].get("Sporting Goods", [])
        product_id = products[0]["id"] if products else None
        print("Product ID to delete:", product_id)
        self.assertIsNotNone(product_id, "Product was not created successfully")

        # Delete the first product
        url = f"/products/{product_id}"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.delete(url, format="json")

        # Print the response content for debugging
        print("Delete response status code:", response.status_code)
        print("Delete response content:", response.content)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Attempt to get the deleted product
        response = self.client.get(url, format="json")

        # Print the response content for debugging
        print("Get response status code:", response.status_code)
        print("Get response content:", response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify the product list does not include the deleted product
        url = "/products"
        response = self.client.get(url, format="json")
        json_response = json.loads(response.content)

        # Print the response content for debugging
        print("Product list response status code:", response.status_code)
        print("Product list response content:", response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        products = json_response["products_by_category"].get("Sporting Goods", [])
        self.assertTrue(all(product["id"] != product_id for product in products))

    # TODO: Product can be rated. Assert average rating exists.
