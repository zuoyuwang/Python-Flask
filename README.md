# a2-zuoyu wang, anyue huang

Run the main Flask server module by running `python3 PizzaParlour.py`

**Be sure to run the server before using the Command line interface and tests**

Run the Command line interface by running `python3 Command.py`

**Follow the instructions and you will have fun with shopping pizza!**

Run unit tests with coverage by running `pytest --cov-report term --cov=. tests/unit_tests.py`

**If you have run the tests once, please restart the server before the second time.** 
**Otherwise the tests may show errors because the order number has been changed**

# Flask Server guidance:
The server will be host in default port "localhost:5000". 

**Path `/pizza` is responsible for orders. You can send following requests:**

* **POST**: To create new order by receiving data with json type. Following is an example data body:


    ```
    {"pizza": [{"size": "small",
               "type": "pepperoni",
               "toppings": {"olives": 2, "mushrooms": 1,"beef": 1}}],
     "drinks": {"Coke": 2},
     "delivery": "pickup"}`
* **GET**: To get order by order number in url `/pizza?number=xxx`.

* **DELETE**: To delete order by order number in url `/pizza?number=xxx`.

* **PUT**: To update order by receiving data with json type. Following are examples data bodies:

For updating `size` or `type`:
    

    {"order number": "4",
     "update": ["pizza", 1（#index for pizza）, "size", "small"]} 
For updating `toppings`:


    {"order number": "2",
     "update": ["pizza", 1（#index for pizza), "toppings", "mushrooms", 2(#new amount)
For updating `drinks`:


    {"order number": "1",
     "update": ["drinks", "Coke", -1(#increase amount)]}`:

**Path `/delivery` is responsible for delivery. You can send following requests:**
* **POST**: To create or update delivery by receiving data with json type. Following is an example data body:

    ```
    {"Order Number": "4",
     "Company": "uber",
     "Address": "1080 Bay street",}
     
**Path `/menu` is responsible for delivery. You can send following requests:**

* **GET**: To get price by item name in url `/menu?name=xxx`.  (input 'all' to get the full menu)
# Pair Programing

### Descriptions:
We basically did pair programing about features of pizza order (`PizzaParlour.py`). Following describe how we did it:

##### First part:
***Driver:*** Anyue Huang
***Navigator:*** Zuoyu Wang
***Feature:*** Create Order, get Order

##### Second part:
***Driver:*** Zuoyu Wang
***Navigator:*** Anyue Huang
***Feature:*** Update Order, Cancel Order

### Reflection:
Totally, the pair programing went pretty well since we took a few hours to make a "blueprint" before we started. After we got the ideas, coding became easy and fast. We dont even ask much questions as a driver.

##### What we liked: 
Feels like we are doing real teamworks. We used to work in a team but more like doing stuff in different parts on our own and form into a big one. Now with pair programing, instead of one person one part, we get a chance to present each part of our code with the best design among two of us.

##### What we disliked:
It takes longer than before to form a project. Usually in a 2 members team, each of us do 1/2 works and then put it together. However, with pair programing, each of us need to do about 100% work since we need to give effert no matter as a driver or navigator.

# Code Craftsmanship

We use [pycharm](https://www.jetbrains.com/pycharm/) for writing the code.

We also use [Pylint](https://www.pylint.org/) to check and format our code.

# Design Pattern
##### Dependency Injection:
(`create_order()`, `get_order()`, `update_order()`, `create_delivery()`, `cancel_order()`)
We use this pattern since we want to make sure we programe into interface but not implementation. Usually, dependencies are declared through interfaces and we use `try` and `except` instead in python.

##### Single Responsibility Principle:
Every function we design follows Single Responsibility Principle, where every fuction represent only one specific functionality.
eg:`update_order()`, `create_order()`, `get_order()`.