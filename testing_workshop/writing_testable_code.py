# Some general tips for writing highly testable code

# Write small functions that do one thing
#region
# Instead of writing a single large function that does many things, 
# break it down into smaller functions that each do one specific task. 
# For example, instead of writing a function that reads a file, 
# processes the data, and writes the output to a database, 
# break it down into separate functions for each task.

# A simple function that does not need to be broken down
def add_numbers(a, b):
    return a + b

# A complex function needs to be broken down
# So that we can test all components in isolation
def process_data(data):
    # Step 1: Clean the data
    cleaned_data = clean_data(data)
    
    # Step 2: Analyze the data
    analysis = analyze_data(cleaned_data)
    
    # Step 3: Save the results
    save_results(analysis)
    
def clean_data(data):
    # Code to clean the data goes here
    pass
    
def analyze_data(data):
    # Code to analyze the data goes here
    pass
    
def save_results(results):
    # Code to save the results goes here
    pass

#endregion

# Avoid side effects.
#region
# If you must have side effects, make them explicit
# Side effects are changes that a function makes to the state of the program 
# outside of its own scope. To make them explicit, you can return the new 
# state of the program as a result of the function. For example, instead of
# modifying a global variable inside a function, return the new value of the 
# variable as the result of the function.
# Try to layer your code in a way to push all side effects into the smallest area possible.
# And try make all other code stateless

# Counterexample: A function that is designed to modify the state of the program
counter = 0
def analyze_data():
    global counter
    if counter > 10:
        counter -= 1
    pass

def increment_counter():
    global counter
    analyze_data()
    counter += 1

# Example: A function with side effects that should be made explicit
def process_data(data):
    # Step 1: Clean the data
    cleaned_data = clean_data(data)
    
    # Step 2: Analyze the data
    analysis = analyze_data(cleaned_data)
    
    # Step 3: Save the results
    results = save_results(analysis)
    
    # Return the new state of the program
    return results
    
def clean_data(data):
    # Code to clean the data goes here
    pass
    
def analyze_data(data):
    # Code to analyze the data goes here
    pass
    
def save_results(results):
    new_results = results.deepcopy()
    # Code to save the results goes here
    # Return the new state of the program
    return new_results

#endregion

# Avoid tight coupling
#region
# Tight coupling is when two pieces of code are dependent on each other. 
# To avoid tight coupling, make sure that each piece of code is independent 
# and can be tested in isolation. For example, instead of calling a function 
# from another function directly, pass the function as an argument to the 
# calling function.

class Database:
    def __init__(self):
        self.data = {}

    def save(self, key, value):
        self.data[key] = value

class User:
    def __init__(self, name):
        self.name = name
        self.db = Database()

    def save(self):
        self.db.save(self.name, self)

user1 = User("Alice")
user1.save()

# In this example, the User and Database classes are tightly coupled because 
# the User class creates an instance of the Database class in its constructor 
# and calls its save method directly. This makes it difficult to test the User 
# class in isolation, because it requires an instance of the Database class to be 
# created and configured.

# Fix:
# region
# To avoid tight coupling, we can use dependency injection to pass in the required 
# dependencies as arguments. Here's an example of how we can refactor the above code:

class Database:
    def __init__(self):
        self.data = {}

    def save(self, key, value):
        self.data[key] = value

class User:
    def __init__(self, name, db):
        self.name = name
        self.db = db

    def save(self):
        self.db.save(self.name, self)

db = Database()
user1 = User("Alice", db)
user1.save()
#endregion

#endregion

# Avoid mutable state
#region
# Mutable state is data that can be changed after it is created. 
# To avoid mutable state, use immutable data structures whenever possible. 
# For example, instead of using a list to store data that is modified frequently, 
# use a tuple or a named tuple that cannot be modified.

class CartItem:
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return self.name
    
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

cart = ShoppingCart()
apple = CartItem("apple")
cart.add_item(apple)
banana = CartItem("banana")
cart.add_item(banana)
cart.remove_item(apple)

print(cart.items)

# In the above example, the items list in the ShoppingCart class is mutable. 
# This can lead to unexpected behavior if the list is modified in one part 
# of the code and then accessed in another part of the code.

# Fix:
# region
from collections import namedtuple

Item = namedtuple("Item", ["name", "price"])

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

cart = ShoppingCart()
cart.add_item(Item("apple", 1.0))
cart.add_item(Item("banana", 2.0))
cart.remove_item(Item("apple", 1.0))

# In the above example, the items list in the ShoppingCart class is replaced with 
# a list of named tuples. Named tuples are immutable, so the items list 
# cannot be modified after it is created. 
# This avoids mutable state and makes the code easier to reason about.
# endregion

#endregion

# Avoid global state
#region
# Global state is data that is accessible from anywhere in the program. 
# To avoid global state, use function arguments and return values to pass 
# data between functions. For example, instead of using a global variable 
# to store a configuration value, pass the value as an argument to the 
# functions that need it.

CONFIG = {
    "debug": True,
    "log_level": "INFO"
}

def log(message):
    if CONFIG["debug"]:
        print(f"[{CONFIG['log_level']}] {message}")

log("This is a debug message")

# In the above example, the CONFIG dictionary is a global variable that is 
# accessible from anywhere in the program. 
# This makes it difficult to reason about the behavior of the log function, 
# because the CONFIG dictionary can be modified from anywhere in the program.

# Fix:
# region
def log(message, debug=False, log_level="INFO"):
    if debug:
        print(f"[{log_level}] {message}")

log("This is a debug message", debug=True, log_level="INFO")

# In the above example, the CONFIG dictionary is replaced with function arguments. 
# This makes it easier to reason about the behavior of the log function, 
# because the function arguments are explicitly passed to the function. 
# This avoids global state and makes the code easier to test and maintain.
# endregion

#endregion

# Use dependency injection
#region
# Dependency injection is a technique for passing dependencies into a function or object,
# rather than creating them inside the function or object. 
# This makes it easier to test code in isolation, 
# because you can replace the dependencies with mock objects or test doubles.

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def calculate_total_price(self):
        total_price = 0
        for item in self.items:
            total_price += item.price
        return total_price

class Order:
    def __init__(self):
        self.cart = ShoppingCart()

    def add_item_to_cart(self, item):
        self.cart.add_item(item)

    def calculate_total_price(self):
        return self.cart.calculate_total_price()

order = Order()
order.add_item_to_cart(Item("apple", 1.0))
order.add_item_to_cart(Item("banana", 2.0))
total_price = order.calculate_total_price()

# In the above example, the Order class creates a new instance of the ShoppingCart class 
# inside its constructor. This makes it difficult to test the Order class in isolation,
# because it is tightly coupled with the ShoppingCart class.

# Fix:
# region
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def calculate_total_price(self):
        total_price = 0
        for item in self.items:
            total_price += item.price
        return total_price

class Order:
    def __init__(self, cart):
        self.cart = cart

    def add_item_to_cart(self, item):
        self.cart.add_item(item)

    def calculate_total_price(self):
        return self.cart.calculate_total_price()

cart = ShoppingCart()
order = Order(cart)
order.add_item_to_cart(Item("apple", 1.0))
order.add_item_to_cart(Item("banana", 2.0))
total_price = order.calculate_total_price()

# In the above example, the Order class is modified to accept an instance of 
# the ShoppingCart class as a constructor argument. 
# This makes it easier to test the Order class in isolation, 
# because we can pass in a mock ShoppingCart object for testing purposes. 
# This avoids tight coupling and makes the code easier to test and maintain.
# endregion

#endregion

# In the end, writing testable code is writing clean and maintainable code. 
# It will benefit you in multiple ways.

# How to cover existing codebase with tests?
#region
# If you have a large codebase without tests, it can be difficult to add tests to it.
# Here are some strategies for adding tests to an existing codebase:

# - Key Insight: Start small. Keep up a routine. Make it a habbit. 
#   A team of 2 developers, who add 2 tests 3 times a week can add 48 tests in a month
# - Key Insight 2: Use Copilot and ChatGPT
# - Add time to write tests to your dev estimates
# - Add tests when you fix bugs. This will help prevent the bugs from reoccurring
# - Use mocking liberally to ease the process of adding tests
# - Break up complex functions into smaller functions that are easier to test
# - Start with the most important parts of the codebase
# - Start with the parts of the codebase that are easiest to test
# - Start with the parts of the codebase that are most likely to change or bereak
# endregion