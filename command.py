"""Command line interface"""
import json
import requests as re

WARNING = "!!!Invalid input!!!"
INT_WAR = "!!!Please input a number!!!"
FAIL_WAR = "!!!Failed!!!Please check your input and try again"
GOODBYE = "Bye, have a nice day!"
S_MSG = "!!!Success!!!"
PORT = "http://127.0.0.1:5000/"
MENU_URL = PORT + "menu?name="
ORDER_URL = PORT + "pizza"
DE_URL = PORT + "delivery"
NO_WAR, FORMAT_WAR, CAN_MSG = ("No such order or item!", "Wrong format!",
                               "Cancel Successfully")


def welcome():
    """Welcome"""
    print("========Welcome to PizzaParlour!========\n")
    print("====What would you like to do? (Type the number)====\n"
          "1. create new order\n"
          "2. Update an existing order\n"
          "3. Getting our menu\n"
          "4. Quit")
    action = input("Choose a number: ")
    return action


# 1. create new order
def new_order():
    """create new order"""
    print("====What would you like to order? (Type the number)====\n"
          "1. Pizza\n"
          "2. Drinks\n"
          "3. Back to main page\n")
    action = input("Choose a number: ")
    while action != "3":
        if action == "1":
            order("pizza")
            return "pizza"
        if action == "2":
            order("drink")
            return "drink"
        print(WARNING)
        print("====What would you like to order? (Type the number)====\n"
              "1. Pizza\n"
              "2. Drinks\n"
              "3. Back to main page\n")
        action = input("Choose a number: ")
    return "3"


# helper functions for create new order
def c_pizza():
    """create new pizza"""
    print("====Choose your size from below====")
    print("==small, medium, large==")
    size = input("Type the choice:")
    print("====Choose your type from below====")
    print("==pepperoni, margherita, vegetarian, Neapolitan, Customize==")
    pizza_type = input("Type the choice:")
    top_d = {}
    print("====Choose your toppings from below====")
    print(
        "==olives, tomatoes, mushrooms, jalapenos, chicken, beef, pepperoni==")
    print("==type 'finish' to finish choosing==")
    top = input("Type the choice:")
    while top != "finish":
        num = input("number of " + top + ": ")
        while not num.isdigit():
            print(INT_WAR)
            num = input("number of " + top + ": ")
        top_d[top] = int(num)
        print("====Choose your toppings from below====")
        print("==olives, tomatoes, mushrooms, jalapenos, chicken, " +
              "beef, pepperoni==")
        print("==type 'finish' to finish choosing toppings==")
        top = input("Type the choice:")
    return {"size": size, "type": pizza_type, "toppings": top_d}


def c_drink():
    """create new drink"""
    print("====Choose your drink from below====")
    print("==Coke, Diet Coke, Coke Zero, Pepsi, Diet Pepsi, " +
          "Dr. Pepper, Water, Juice==")
    drink = input("Type the choice:")
    num = input("number of " + drink + ": ")
    while not num.isdigit():
        print(INT_WAR)
        num = input("number of " + drink + ": ")
    return drink, int(num)


def order(pizza_or_drink):
    """init order"""
    pizza_list = []
    drink_d = {}
    if pizza_or_drink == "pizza":
        pizza = c_pizza()
        pizza_list.append(pizza)
    else:
        drink, num = c_drink()
        drink_d[drink] = num
    print("====What else would you like? (Type the number)====\n"
          "1. Pizza\n"
          "2. Drinks\n"
          "3. Confirm\n")
    action = input("Choose a number: ")
    while action != "3":
        if action == "1":
            pizza = c_pizza()
            pizza_list.append(pizza)
        elif action == "2":
            drink, num = c_drink()
            drink_d[drink] = num
        else:
            print(WARNING)
        print("====What else would you like? (Type the number)====\n"
              "1. Pizza\n"
              "2. Drinks\n"
              "3. Confirm\n")
        action = input("Choose a number: ")
    order_c = {"pizza": pizza_list, "drinks": drink_d, "delivery": ""}
    msg = order_server(order_c)
    if msg == FORMAT_WAR:
        print(FAIL_WAR)
        return "error"
    print(S_MSG)
    msg1 = delivery(str(msg["order number"]))
    while msg1 == NO_WAR:
        print(WARNING)
        msg1 = delivery(str(msg["order number"]))
    print(S_MSG)
    print("===Below is your order and delivery detail: ===")
    print("Order: ", msg)
    if msg1["Company"] != "pickup":
        print("Delivery: ", msg1)
        return msg1["Company"]
    return "pickup"


def delivery(order_num):
    """create delivery"""
    print("====Choose your delivery method (Type the number)====\n"
          "===pickup, uber, Foodora===\n")
    company = input("Type the choice: ")
    address = ""
    if company != "pickup":
        address = input("====Type your Address====\n")
    delivery1 = {"Order Number": order_num, "Company": company,
                 "Address": address}
    msg = de_server(delivery1)
    if msg == NO_WAR:
        return msg
    return delivery1


# 2. update order or delivery
def update_od():
    """update order or delivery"""
    print("====What your order number?====\n")
    num = input("Order number: ")
    while not num.isdigit():
        print(INT_WAR)
        num = input("Order number: ")
    order1 = order_get(num)
    while order1 == NO_WAR:
        print(NO_WAR)
        num = input("Order number: ")
        order1 = order_get(num)
    print("Here is your order: ", order1)
    print("====What do your want to update?====\n"
          "1. Pizza and Drink\n"
          "2. Delivery Method\n"
          "3. Cancel Order\n"
          "4. Back to main page\n")
    action = input("Choose a number: ")
    while action not in ("1", "2", "3", "4"):
        print(WARNING)
        action = input("Choose a number: ")
    if action == "1":
        msg_pd = update_pd(str(num), order1["details"])
        while msg_pd == NO_WAR:
            print(WARNING)
            msg_pd = update_pd(str(num), order1["details"])
        print(S_MSG)
        print("===Your new order detail: ===")
        print(msg_pd)
    elif action == "2":
        msg_d = delivery(str(num))
        while msg_d == NO_WAR:
            print(WARNING)
            msg_d = delivery(str(num))
        print(S_MSG)
        print("===Your new delivery: ===")
        if msg_d["Company"] != "pickup":
            print(msg_d)
        else:
            print("pickup")
    elif action == "3":
        msg_c = order_cancel(num)
        print(msg_c)
    else:
        pass
    return action


# helper for updating pizza or drink
def update_pd(num, detail):
    """ Update pizza or drink"""
    update_l = []
    print("Here is the pizza and drink detail: ", detail)
    print("===Update what?===\n"
          "pizza, drinks")
    pizza_drink = input("Select: ")
    update_l.append(pizza_drink)
    if pizza_drink == "pizza":
        print("Here is the pizza detail: ", detail["pizza"])
        print("===Which pizza do you want to update on?===")
        index = input("Type the index(Starting from 0): ")
        while not index.isdigit():
            print(INT_WAR)
            index = input("Type the index(Starting from 0): ")
        while int(index) >= len(detail["pizza"]):
            print(WARNING)
            index = input("Type the index(Starting from 0): ")
        update_l.append(int(index))
        print("Here is the detail: ", detail["pizza"][int(index)])
        print("===What do you want to update?===\n"
              "==size, type, toppings==")
        stp = input("Type the choice: ")
        update_l.append(stp)
        if stp == "size":
            print("Your size now: ", detail["pizza"][int(index)]["size"])
            print("====Choose your new size from below====")
            print("==small, medium, large==")
            size = input("Type the choice:")
            update_l.append(size)
        elif stp == "type":
            print("Your type now: ", detail["pizza"][int(index)]["type"])
            print("====Choose your type from below====")
            print(
                "==pepperoni, margherita, vegetarian, Neapolitan, Customize==")
            pizza_type = input("Type the choice:")
            update_l.append(pizza_type)
        elif stp == "toppings":
            print("Your toppings now: ",
                  detail["pizza"][int(index)]["toppings"])
            top = input("Select the one you want to update: ")
            t_num = input("New number: ")
            while not t_num.isdigit():
                print(INT_WAR)
                t_num = input("New number: ")
            update_l.append(top)
            update_l.append(int(t_num))
    elif pizza_drink == "drinks":
        print("Here is the drink detail: ", detail["drinks"])
        drink = input("Select the one you want to update: ")
        dr_num = input("New number: ")
        while not dr_num.isdigit():
            print(INT_WAR)
            dr_num = input("New number: ")
        update_l.append(drink)
        update_l.append(int(dr_num))
    update_d = {"order number": num,
                "update": update_l}
    print(update_d)
    data = order_update(update_d)
    return data


# 3.get menu
def menu():
    """ Get menu"""
    dic = menu_get("all")
    item = {"Drinks": list(dic["Drinks"].keys()), "Pizza": {}}
    item["Pizza"]["size"] = list(dic["Pizza"]['size'].keys())
    item["Pizza"]["type"] = list(dic["Pizza"]['type'].keys())
    item["Pizza"]["toppings"] = list(dic["Pizza"]['toppings'].keys())

    print("====Which item would you like to know?====")
    print(item)
    print("==Type 'all' to show the full menu or the specific item name==\n"
          "==Type 'back' to return to main page==")
    name = input("Item: ")
    check = None
    while name != "back":
        if name == "all":
            print(dic)
            check = "all"
        else:
            price = str(menu_get(name))
            if price == NO_WAR:
                print(price)
                check = NO_WAR
            else:
                print("The price for " + name + " is " + price)
                check = "success"
        print("==Type 'all' to show the full menu or the specific item name==\n"
              "==Type 'back' to return to main page==")
        name = input("Item: ")
    return check


def order_server(order1):
    """create order on server"""
    response = re.post(ORDER_URL, json=order1)
    data = json.loads(response.content)
    return data


def de_server(delivery1):
    """create or update delivery on server"""
    response = re.post(DE_URL, json=delivery1)
    data = json.loads(response.content)
    return data


def menu_get(name):
    """get menu from server"""
    response = re.get(MENU_URL + name)
    data = json.loads(response.content)
    return data


def order_get(num):
    """get order from server"""
    response = re.get(ORDER_URL + "?number=" + num)
    data = json.loads(response.content)
    return data


def order_update(update_d):
    """update order from server"""
    response = re.put(ORDER_URL, json=update_d)
    data = json.loads(response.content)
    return data


def order_cancel(num):
    """cancel order from server"""
    response = re.delete(ORDER_URL + "?number=" + num)
    data = json.loads(response.content)
    return data


def main():
    """main function"""
    action = welcome()
    while action != "4":
        if action == "1":
            new_order()
        elif action == "2":
            update_od()
        elif action == "3":
            menu()
        else:
            print(WARNING)
        action = welcome()
    print(GOODBYE)
    return action


if __name__ == "__main__":
    main()
