"""
Module for pizza server
"""
import json
from flask import Flask, request, jsonify

APP = Flask("Assignment 2")


def load_file():
    """load message and price constants"""
    with open('./price.json') as json_file:
        data = json.load(json_file)
    return (data["size"], data["type"], data["topping"], data["drink"],
            data["message"]["No warning"], data["message"]["Format warning"],
            data["message"]["Cancel message"])


def load_order():
    """load pre-defined order"""
    with open('./order.json') as json_file:
        data = json.load(json_file)
    return data


def load_delivery():
    """load pre-defined delivery"""
    with open('./delivery.json') as json_file:
        data = json.load(json_file)
    return data


# load menu, message and order
SIZE_D, TYPE_D, TOPPING_D, DRINKS_D, NO_WAR, FORMAT_WAR, CAN_MSG = load_file()
MENU_D = {"Pizza": {"size": SIZE_D, "type": TYPE_D, "toppings": TOPPING_D},
          "Drinks": DRINKS_D}
ORDER_D, DELI_D = load_order(), load_delivery()


@APP.route('/pizza', methods=['POST'])
def create_order():
    """create new order"""
    data = request.json
    try:
        order = form(data)
        ORDER_D[str(order["order number"])] = order
    except Exception:
        return jsonify(FORMAT_WAR)
    return jsonify(order)


@APP.route('/pizza', methods=['GET'])
def get_order():
    """get order by order number"""
    res = NO_WAR
    try:
        number = request.args.get("number")
        res = ORDER_D[number]
    except Exception:
        return jsonify(res)
    return jsonify(res)


# Design Pattern: Dependency Injection
# Instead of directly design an Interface in python,
# we use 'try except' so that we
# program to interface not implementation.

@APP.route('/pizza', methods=['PUT'])
def update_order():
    """ update order by order number"""
    data = request.json
    res = NO_WAR
    try:
        num = data["order number"]
        update_o(num, data["update"])
    except Exception:
        return jsonify(res)
    return jsonify(ORDER_D[num])


@APP.route('/delivery', methods=['POST'])
def create_delivery():
    """ create or update new delivery"""
    data = request.json
    try:
        delivery = form_delivery(data)
    except Exception:
        return jsonify(NO_WAR)
    return jsonify(delivery)


@APP.route('/pizza', methods=['DELETE'])
def cancel_order():
    """ Cancel order"""
    res = NO_WAR
    try:
        number = request.args.get("number")
        del ORDER_D[number]
    except KeyError:
        return jsonify(res)
    return jsonify(CAN_MSG)


@APP.route("/menu", methods=["GET"])
def compute():
    """ get menu"""
    name = request.args.get("name")
    if name == "all":
        res = MENU_D
    elif name in SIZE_D:
        res = SIZE_D[name]
    elif name in TYPE_D:
        res = TYPE_D[name]
    elif name in TOPPING_D:
        res = TOPPING_D[name]
    elif name in DRINKS_D:
        res = DRINKS_D[name]
    else:
        res = NO_WAR
    return jsonify(res)


# helper functions
def form(data):
    """ form order detail"""
    total = 0
    for pizza in data['pizza']:
        size = pizza['size']
        p_type = pizza['type']
        top = pizza['toppings']
        total += SIZE_D[size]
        total += TYPE_D[p_type]
        for item in top:
            total += TOPPING_D[item] * top[item]
    for element in data['drinks']:
        total += DRINKS_D[element] * data['drinks'][element]

    order = {"order number": len(ORDER_D) + 1,
             "details": {"pizza": data["pizza"], "drinks": data["drinks"]},
             "price": total, 'delivery': data['delivery']}
    return order


def form_delivery(data):
    """ form delivery detail"""
    company = data["Company"]
    num = data["Order Number"]
    origin = ORDER_D[num]["delivery"]
    ORDER_D[num]["delivery"] = company
    if origin == "uber" and num in DELI_D["uber"]:
        del DELI_D["uber"][num]
    elif origin == "Foodora" and num in DELI_D["Foodora"]:
        del DELI_D["Foodora"][num]
    if company == "pickup":
        return DELI_D
    detail = ORDER_D[num]["details"]
    delivery = {"Address": data["Address"], "Order Details": detail,
                "Order Number": int(num)}
    if company == "uber":
        DELI_D["uber"][num] = delivery
    elif company == "Foodora":
        DELI_D["Foodora"][num] = delivery
    else:
        raise KeyError
    return DELI_D


def update_o(index, updat) -> None:
    """ update order helper"""
    if updat[0] == "pizza":
        if updat[2] in ("size", "type"):
            orig = ORDER_D[index]['details']["pizza"][updat[1]][updat[2]]
            ORDER_D[index]['details']["pizza"][updat[1]][updat[2]] = updat[3]
            if updat[2] == "size":
                price = SIZE_D[updat[3]] - SIZE_D[orig]
            else:
                price = TYPE_D[updat[3]] - TYPE_D[orig]
        else:
            orig = ORDER_D[index]['details']["pizza"][updat[1]][updat[2]][
                updat[3]]
            ORDER_D[index]['details']["pizza"][updat[1]][updat[2]][
                updat[3]] = updat[4]
            price = (updat[4] - orig) * TOPPING_D[updat[3]]
    elif updat[0] == "drinks":
        orig = ORDER_D[index]['details']["drinks"][updat[1]]
        ORDER_D[index]['details']["drinks"][updat[1]] = updat[2]
        price = DRINKS_D[updat[1]] * (updat[2] - orig)
    else:
        raise KeyError
    ORDER_D[index]["price"] += price


if __name__ == "__main__":
    APP.run()
