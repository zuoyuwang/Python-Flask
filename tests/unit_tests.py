import ast
from pizzaparlour import APP
import unittest
from unittest.mock import patch
from command import *


# test pizzapalour.py
def load_file():
    with open('price.json') as json_file:
        data = json.load(json_file)
    return (data["size"], data["type"], data["topping"], data["drink"],
            data["message"]["No warning"], data["message"]["Format warning"],
            data["message"]["Cancel message"])


def load_order():
    with open('order.json') as json_file:
        data = json.load(json_file)
    return data


# load menu, message and order
SIZE_D, TYPE_D, TOPPING_D, Drinks_D, NO_WAR, FORMAT_WAR, CAN_MSG = load_file()
MENU_D = {"Pizza": {"size": SIZE_D, "type": TYPE_D, "toppings": TOPPING_D},
          "Drinks": Drinks_D}
ORDER_D = load_order()
MOCK_ORDER = {
    "pizza": [{"size": "small",
               "type": "pepperoni",
               "toppings": {"olives": 2, "mushrooms": 1,
                            "beef": 1
                            }}],
    "drinks": {"Coke": 2},
    "delivery": "uber"}

MOCK_UPDATE = [{"order number": "2",
                "update": ["pizza", 0, "toppings", "mushrooms", 5]},
               {"order number": "1",
                "update": ["drinks", "Coke", 1]},
               {"order number": "3",
                "update": ["pizza", 0, "size", "small"]},
               {"order number": "3",
                "update": ["pizza", 0, "type", "pepperoni"]},
               {"order number": "400",
                "update": ["pizza", 0, "size", "small"]}
               ]

MOCK_DELIVERY = [{
    "Order Number": "4",
    "Company": "uber",
    "Address": "1080 Bay street",
}, {
    "Order Number": "4",
    "Company": "Foodora",
    "Address": "1080 Bay street",
}, {
    "Order Number": "400",
    "Company": "Foodora",
    "Address": "1080 Bay street",
}, {
    "Order Number": "4",
    "Company": "pickup",
    "Address": "",
}]


def test_create_order():
    response = APP.test_client().post("/pizza",
                                      json=MOCK_ORDER)

    # convert into python dict
    data = ast.literal_eval(response.data.decode('utf-8'))
    order = {'order number': 4,
             "details": {'pizza': [{'size': 'small',
                                    'type': 'pepperoni',
                                    'toppings': {'olives': 2,
                                                 'mushrooms': 1,
                                                 'beef': 1}}],
                         'drinks': {'Coke': 2}},
             'price': 47,
             'delivery': 'uber'}
    assert response.status_code == 200
    assert data == order


def test_get_order():
    response = APP.test_client().get("/pizza?number=1")

    # convert into python dict
    data = ast.literal_eval(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data == ORDER_D["1"]


def test_create_wrong_format():
    response = APP.test_client().post("/pizza", json=ORDER_D)

    # convert into python dict
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data == FORMAT_WAR


def test_get_no_order():
    response = APP.test_client().get("/pizza?number=0")

    # convert into python dict
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data == NO_WAR


def test_update_order_pizza():
    response = APP.test_client().put("/pizza", json=MOCK_UPDATE[0])

    # convert into python dict
    data = ast.literal_eval(response.data.decode('utf-8'))
    order = {'order number': 2,
             "details": {'pizza': [{'size': 'small',
                                    'type': 'pepperoni',
                                    'toppings': {'olives': 1,
                                                 'mushrooms': 5,
                                                 'beef': 1}}],
                         'drinks': {'Coke': 2}},
             'price': 52,
             'delivery': 'Foodora'}
    assert response.status_code == 200
    assert data == order


def test_update_order_drink():
    response = APP.test_client().put("/pizza", json=MOCK_UPDATE[1])

    # convert into python dict
    data = ast.literal_eval(response.data.decode('utf-8'))
    order = {
        "order number": 1,
        "details": {"pizza": [{"size": "small",
                               "type": "pepperoni",
                               "toppings": {"olives": 1,
                                            "mushrooms": 1,
                                            "beef": 1}}],
                    "drinks": {"Coke": 1}},
        "price": 36,
        "delivery": "pickup"}
    assert response.status_code == 200
    assert data == order


def test_update_order_size():
    response = APP.test_client().put("/pizza", json=MOCK_UPDATE[2])

    # convert into python dict
    data = ast.literal_eval(response.data.decode('utf-8'))
    order = {
        "order number": 3,
        "details": {"pizza": [{"size": "small",
                               "type": "Customize",
                               "toppings": {"chicken": 2, }}],
                    "drinks": {"Diet Coke": 1,
                               "Pepsi": 1}},
        "price": 38.5,
        "delivery": "Uber Eats"}
    assert response.status_code == 200
    assert data == order


def test_update_order_type():
    response = APP.test_client().put("/pizza", json=MOCK_UPDATE[3])

    # convert into python dict
    data = ast.literal_eval(response.data.decode('utf-8'))
    order = {
        "order number": 3,
        "details": {"pizza": [{"size": "small",
                               "type": "pepperoni",
                               "toppings": {"chicken": 2, }}],
                    "drinks": {"Diet Coke": 1,
                               "Pepsi": 1}},
        "price": 46.5,
        "delivery": "Uber Eats"}
    assert response.status_code == 200
    assert data == order


def test_update_no_order():
    response = APP.test_client().put("/pizza", json=MOCK_UPDATE[4])

    # convert into python dict
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data == NO_WAR


def test_create_delivery_uber():
    response = APP.test_client().post("/delivery", json=MOCK_DELIVERY[0])

    # convert into python dict
    data = (ast.literal_eval(response.data.decode('utf-8')))["uber"]["4"]
    de = {'Order Number': 4,
          "Order Details": {'pizza': [{'size': 'small',
                                       'type': 'pepperoni',
                                       'toppings': {'olives': 2,
                                                    'mushrooms': 1,
                                                    'beef': 1}}],
                            'drinks': {'Coke': 2}},
          'Address': '1080 Bay street'}
    assert response.status_code == 200
    assert data == de


def test_create_delivery_foodora():
    response = APP.test_client().post("/delivery", json=MOCK_DELIVERY[1])

    # convert into python dict
    data = (ast.literal_eval(response.data.decode('utf-8')))["Foodora"]["4"]
    de = {'Order Number': 4,
          "Order Details": {'pizza': [{'size': 'small',
                                       'type': 'pepperoni',
                                       'toppings': {'olives': 2,
                                                    'mushrooms': 1,
                                                    'beef': 1}}],
                            'drinks': {'Coke': 2}},
          'Address': '1080 Bay street'}
    assert response.status_code == 200
    assert data == de


def test_no_delivery():
    response = APP.test_client().post("/delivery", json=MOCK_DELIVERY[2])

    # convert into python dict
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data == NO_WAR


def test_pickup_delivery():
    response = APP.test_client().post("/delivery", json=MOCK_DELIVERY[3])

    # convert into python dict
    data = (ast.literal_eval(response.data.decode('utf-8')))

    assert response.status_code == 200
    assert len(data["Foodora"]) == 1
    assert len(data["uber"]) == 1


def test_cancel_order():
    response = APP.test_client().delete(
        "http://127.0.0.1:3001/pizza?number=1")

    # convert into python dict
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data == CAN_MSG


def test_all_menu():
    response = APP.test_client().get('/menu?name=all')

    # convert into python dict
    data = ast.literal_eval(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data == MENU_D


def test_invalid_item():
    response = APP.test_client().get('/menu?name=invalid')

    # convert into python dict
    data = ast.literal_eval(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data == NO_WAR


def test_get_drink():
    response = APP.test_client().get('/menu?name=Coke')

    # convert into python dict
    data = ast.literal_eval(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data == 4


def test_get_size():
    response = APP.test_client().get('/menu?name=small')

    # convert into python dict
    data = ast.literal_eval(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data == 10


def test_get_topping():
    response = APP.test_client().get('/menu?name=jalapenos')

    # convert into python dict
    data = ast.literal_eval(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data == 4


def test_get_type():
    response = APP.test_client().get('/menu?name=Customize')

    # convert into python dict
    data = ast.literal_eval(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data == 10


# test command.py
class Test(unittest.TestCase):
    @patch('builtins.input', side_effect=["10", "2"])
    def test01_welcome(self, mock_input):
        action = welcome()
        action2 = welcome()
        self.assertEqual(action, '10')
        self.assertEqual(action2, '2')

    @patch('builtins.input', side_effect=["1", "2", "3", "4", "1"])
    @patch("command.order", side_effect=[None, None, None])
    def test02_new_order(self, mock_input, mock_order):
        t1 = new_order()
        t2 = new_order()
        t3 = new_order()
        t4 = new_order()
        self.assertEqual(t1, 'pizza')
        self.assertEqual(t2, 'drink')
        self.assertEqual(t3, "3")
        self.assertEqual(t4, 'pizza')

    @patch('builtins.input',
           side_effect=["small", "pepperoni", "tomatoes", "4qwiej", "1",
                        "finish"])
    def test03_c_pizza(self, mock_input):
        t1 = c_pizza()
        d = {"size": "small", "type": "pepperoni", "toppings": {"tomatoes": 1}}
        self.assertEqual(t1, d)

    @patch('builtins.input',
           side_effect=["Diet Coke", "asdjfhkj", "3"])
    def test04_c_drink(self, mock_input):
        t1 = c_drink()
        d = ("Diet Coke", 3)
        self.assertEqual(t1, d)

    @patch('builtins.input', side_effect=["1", "2", "4", "3"])
    @patch("command.c_pizza", side_effect=["Mock_pizza1", "Mock_pizza2"])
    @patch("command.c_drink", side_effect=[("Mock_drink", 3)])
    @patch("command.order_server", side_effect=[{"order number": "2"}])
    @patch("command.delivery", side_effect=[NO_WAR, {"Company": "pickup"}])
    def test05_order_pizza(self, mock_input, mock_c_pizza, mock_c_drink,
                           mock_order_server, mock_delivery):
        t1 = order("pizza")
        self.assertEqual(t1, "pickup")

    @patch('builtins.input', side_effect=["3"])
    @patch("command.c_drink", side_effect=[("Mock_drink", 5)])
    @patch("command.order_server", side_effect=[{"order number": "5"}])
    @patch("command.delivery", side_effect=[{"Company": "uber"}])
    def test06_order_drink(self, mock_input, mock_c_drink,
                           mock_order_server, mock_delivery):
        t1 = order("drink")
        self.assertEqual(t1, "uber")

    @patch('builtins.input', side_effect=["3"])
    @patch("command.c_drink", side_effect=[("Mock_drink", 5)])
    @patch("command.order_server", side_effect=[FORMAT_WAR])
    def test07_order_error(self, mock_input, mock_c_drink, mock_order_server):
        t1 = order("drink")
        self.assertEqual(t1, "error")

    @patch('builtins.input', side_effect=["uber", "Mock_address", "pickup"])
    @patch("command.de_server", side_effect=["Mock_msg", NO_WAR])
    def test08_delivery(self, mock_input, mock_de_server):
        t1 = delivery('2')
        t2 = delivery('3')
        de = {"Order Number": "2", "Company": "uber", "Address": "Mock_address"}
        self.assertEqual(t1, de)
        self.assertEqual(t2, NO_WAR)

    @patch('builtins.input',
           side_effect=["pizza", "adef", "100", "0", "size", "large"])
    @patch("command.order_update", side_effect=[
        {"order number": 3, "update": ["pizza", 0, "size", "large"]}])
    def test09_update_size(self, mock_input, mock_order_update):
        t1 = update_pd(3, {"pizza": [{"size": "small",
                                      "type": "pepperoni",
                                      "toppings": {
                                          "olives": 1,
                                          "mushrooms": 1,
                                          "beef": 1}}],
                           "drinks": {"Coke": 2}})
        update_d = {"order number": 3, "update": ["pizza", 0, "size", "large"]}
        self.assertEqual(t1, update_d)

    @patch('builtins.input',
           side_effect=["pizza", "0", "type", "pepperoni"])
    @patch("command.order_update", side_effect=[
        {"order number": 7, "update": ["pizza", 0, "type", "pepperoni"]}])
    def test10_update_type(self, mock_input, mock_order_update):
        t1 = update_pd(7, {"pizza": [{"size": "small",
                                      "type": "pepperoni",
                                      "toppings": {
                                          "olives": 1,
                                          "mushrooms": 1,
                                          "beef": 1}}],
                           "drinks": {"Coke": 2}})
        update_d = {"order number": 7,
                    "update": ["pizza", 0, "type", "pepperoni"]}
        self.assertEqual(t1, update_d)

    @patch('builtins.input',
           side_effect=["pizza", "0", "toppings", "olives", "aaaa", "3"])
    @patch("command.order_update", side_effect=[
        {"order number": 1, "update": ["pizza", 0, "toppings", "olives", 3]}])
    def test11_update_toppings(self, mock_input, mock_order_update):
        t1 = update_pd(1, {"pizza": [{"size": "small",
                                      "type": "pepperoni",
                                      "toppings": {
                                          "olives": 1,
                                          "mushrooms": 1,
                                          "beef": 1}}],
                           "drinks": {"Coke": 2}})
        update_d = {"order number": 1,
                    "update": ["pizza", 0, "toppings", "olives", 3]}
        self.assertEqual(t1, update_d)

    @patch('builtins.input',
           side_effect=["drinks", "Coke", "5"])
    @patch("command.order_update", side_effect=[
        {"order number": 4, "update": ["drinks", "Coke", 5]}])
    def test12_update_drink(self, mock_input, mock_order_update):
        t1 = update_pd(4, {"pizza": [{"size": "small",
                                      "type": "pepperoni",
                                      "toppings": {
                                          "olives": 1,
                                          "mushrooms": 1,
                                          "beef": 1}}],
                           "drinks": {"Coke": 2}})
        update_d = {"order number": 4,
                    "update": ["drinks", "Coke", 5]}
        self.assertEqual(t1, update_d)

    @patch('builtins.input', side_effect=["all", "back"])
    @patch("command.menu_get", side_effect=[MENU_D])
    def test13_menu_all(self, mock_input, mock_menu_get):
        t1 = menu()
        self.assertEqual(t1, "all")

    @patch('builtins.input', side_effect=["Coke", "back"])
    @patch("command.menu_get", side_effect=[MENU_D, "Coke"])
    def test14_menu_item(self, mock_input, mock_menu_get):
        t1 = menu()
        self.assertEqual(t1, "success")

    @patch('builtins.input', side_effect=["Coke", "back"])
    @patch("command.menu_get", side_effect=[MENU_D, NO_WAR])
    def test15_menu_wrong(self, mock_input, mock_menu_get):
        t1 = menu()
        self.assertEqual(t1, NO_WAR)

    def test16_order_server(self):
        data = order_server(MOCK_ORDER)
        expect = {'order number': 4,
                  "details": {'pizza': [{'size': 'small',
                                         'type': 'pepperoni',
                                         'toppings': {'olives': 2,
                                                      'mushrooms': 1,
                                                      'beef': 1}}],
                              'drinks': {'Coke': 2}},
                  'price': 47,
                  'delivery': 'uber'}
        self.assertEqual(expect, data)

    def test17_menu_get(self):
        data = menu_get("all")
        self.assertEqual(MENU_D, data)

    def test18_order_get(self):
        data = order_get("4")
        expect = {"order number": 4,
                  "details": {"pizza": [{"size": "small",
                                         "type": "pepperoni",
                                         "toppings": {
                                             "olives": 2,
                                             "mushrooms": 1,
                                             "beef": 1}}],
                              "drinks": {"Coke": 2}},
                  "price": 47,
                  "delivery": "uber"}
        self.assertEqual(expect, data)

    def test19_order_update(self):
        data = order_update(MOCK_UPDATE[0])
        order_up = {'order number': 2,
                    "details": {'pizza': [{'size': 'small',
                                           'type': 'pepperoni',
                                           'toppings': {'olives': 1,
                                                        'mushrooms': 5,
                                                        'beef': 1}}],
                                'drinks': {'Coke': 2}},
                    'price': 52,
                    'delivery': 'Foodora'}
        self.assertEqual(data, order_up)

    def test20_order_cancel(self):
        data = order_cancel("3")
        self.assertEqual(data, CAN_MSG)

    @patch("command.welcome", side_effect=["1", "2", "3", "4123123", "4"])
    @patch("command.new_order", side_effect=[None])
    @patch("command.update_od", side_effect=[None])
    @patch("command.menu", side_effect=[None])
    def test21_main(self, mock_welcome, mock_new_order, mock_update_od,
                    mock_menu):
        t1 = main()
        self.assertEqual(t1, "4")

    @patch('builtins.input',
           side_effect=["asdf", "10", "1", "5", "1"])
    @patch("command.order_get", side_effect=[NO_WAR, {
        "delivery": "pickup",
        "details": {"drinks": {"Coke": 2},
                    "pizza": [{"size": "small", "toppings": {"beef": 1,
                                                             "mushrooms": 1,
                                                             "olives": 1},
                               "type": "pepperoni"}]},
        "order number": 1,
        "price": 40}])
    @patch("command.update_pd", side_effect=[NO_WAR, S_MSG])
    def test22_update_pizza_drink(self, mock_input, mock_order_get, mock_update_pd):
        t1 = update_od()
        self.assertEqual(t1, "1")
