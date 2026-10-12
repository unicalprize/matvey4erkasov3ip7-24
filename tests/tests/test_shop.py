import unittest
from shop import (
    get_low_stock,
    search_advanced,
    total_sum,
    cart_total,
    add_to_cart,
    remove_from_cart,
    update_quantity,
)


# ---------- Задание 2: тесты функций каталога ----------

class TestGetLowStock(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(get_low_stock([]), [])

    def test_no_low_stock(self):
        products = [{'name': 'A', 'sizes': {40: 10}}]
        self.assertEqual(get_low_stock(products), [])

    def test_one_low_stock(self):
        products = [
            {'name': 'A', 'sizes': {40: 1}},
            {'name': 'B', 'sizes': {40: 10}},
        ]
        result = get_low_stock(products)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'A')


class TestSearchAdvanced(unittest.TestCase):
    def setUp(self):
        self.products = [
            {'id': 1, 'name': 'Футболка', 'category': 'одежда', 'price': 1000, 'sizes': {40: 5}},
            {'id': 2, 'name': 'Кроссовки', 'category': 'обувь', 'price': 5000, 'sizes': {41: 3}},
            {'id': 3, 'name': 'Кепка', 'category': 'аксессуары', 'price': 800, 'sizes': {}},
        ]

    def test_search_by_name(self):
        result = search_advanced(self.products, name='фут')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Футболка')

    def test_search_by_category(self):
        result = search_advanced(self.products, category='обувь')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Кроссовки')

    def test_search_by_max_price(self):
        result = search_advanced(self.products, max_price=1000)
        names = [p['name'] for p in result]
        self.assertIn('Футболка', names)
        self.assertIn('Кепка', names)
        self.assertNotIn('Кроссовки', names)

    def test_search_no_filters(self):
        result = search_advanced(self.products)
        self.assertEqual(len(result), 3)


class TestTotalSum(unittest.TestCase):
    def test_empty_cart(self):
        self.assertEqual(total_sum([]), 0)

    def test_sum_with_products(self):
        products = [{'price': 100}, {'price': 250}, {'price': 50}]
        self.assertEqual(total_sum(products), 400)


# ---------- Задание 3: тесты с ожидаемыми ошибками ----------

class TestAddToCart(unittest.TestCase):
    def test_invalid_size(self):
        products = [{'id': 1, 'name': 'A', 'sizes': {40: 5}, 'price': 100}]
        cart = []
        result, message = add_to_cart(cart, products, 1, 99, 1)
        self.assertFalse(result)
        self.assertIn('размер', message.lower())

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            _ = 1 / 0


# ---------- Задание 5: тесты корзины ----------

class TestCart(unittest.TestCase):
    def setUp(self):
        self.products = [
            {'id': 1, 'name': 'Футболка', 'sizes': {40: 5}, 'price': 1000},
            {'id': 2, 'name': 'Джинсы', 'sizes': {42: 2}, 'price': 3000},
        ]

    def test_add_to_cart_success(self):
        cart = []
        result, _ = add_to_cart(cart, self.products, 1, 40, 2)
        self.assertTrue(result)
        self.assertEqual(len(cart), 1)
        self.assertEqual(cart[0]['quantity'], 2)

    def test_add_to_cart_twice_increases_quantity(self):
        cart = []
        add_to_cart(cart, self.products, 1, 40, 1)
        add_to_cart(cart, self.products, 1, 40, 2)
        self.assertEqual(len(cart), 1)
        self.assertEqual(cart[0]['quantity'], 3)

    def test_remove_from_cart(self):
        cart = []
        add_to_cart(cart, self.products, 1, 40, 1)
        result = remove_from_cart(cart, 1, 40)
        self.assertTrue(result)
        self.assertEqual(cart, [])

    def test_remove_from_cart_not_found(self):
        cart = []
        self.assertFalse(remove_from_cart(cart, 99, 99))

    def test_update_quantity(self):
        cart = []
        add_to_cart(cart, self.products, 1, 40, 1)
        update_quantity(cart, 1, 40, 5)
        self.assertEqual(cart[0]['quantity'], 5)

    def test_update_quantity_zero_removes_item(self):
        cart = []
        add_to_cart(cart, self.products, 1, 40, 1)
        update_quantity(cart, 1, 40, 0)
        self.assertEqual(cart, [])

    def test_cart_total(self):
        cart = []
        add_to_cart(cart, self.products, 1, 40, 2)   # 1000 * 2 = 2000
        add_to_cart(cart, self.products, 2, 42, 1)   # 3000 * 1 = 3000
        self.assertEqual(cart_total(cart), 5000)

    def test_cart_total_empty(self):
        self.assertEqual(cart_total([]), 0)


if __name__ == '__main__':
    unittest.main()