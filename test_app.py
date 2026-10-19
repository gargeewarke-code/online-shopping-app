import unittest
from app import app, cart


class ShoppingAppTests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        cart.clear()

    def tearDown(self):
        cart.clear()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Online Shopping Application", response.data)

    def test_search_product(self):
        response = self.client.get("/?search=Laptop")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertNotIn(b"Headphones", response.data)

    def test_add_to_cart(self):
        response = self.client.get("/add/1")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(cart), 1)

    def test_order_empty_cart(self):
        response = self.client.get("/order")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Your cart is empty", response.data)


if __name__ == "__main__":
    unittest.main()