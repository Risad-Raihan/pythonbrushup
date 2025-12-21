# Understanding Python Classes: Let's Build a Virtual Microwave!

<img src="infographic.png" alt="Understanding Python Classes – Virtual Microwave" width="700"/>

## 1. Introduction: What is a Class? The Blueprint Analogy


Before a house is built, an architect creates a blueprint. This blueprint isn't the house itself; it's the detailed plan that defines what the house will look like and how it will function. It specifies the number of rooms, the location of doors, and the layout of the plumbing. From that single blueprint, you can build many identical houses.

In Python, a **class** serves the exact same purpose. It’s not the final object, but the design plan for creating objects.

A class is just a blueprint for what an object should look like and how it should function.

In this guide, we'll step into the role of a virtual microwave manufacturer. We will first design the blueprint for a `Microwave` class. Then, using that blueprint, we will "manufacture" unique microwave objects, each with its own specific details and functions.

Let's begin by drafting our first, simple blueprint in Python.

### 2. Creating Our First (Empty) Blueprint

#### The `class` Keyword

To create a blueprint in Python, we use the `class` keyword followed by a name. By convention, class names use **CamelCase**, meaning the first letter of each word is capitalized, with no spaces. For example, a class for a blue car would be `BlueCar`.

Let's create our `Microwave` blueprint. For now, it will be completely empty.

#### Building from the Blueprint: Creating an Instance

Just having the blueprint isn't enough; we need to build an actual microwave from it. In programming, this process is called **instantiation**, and the resulting object is called an **instance**.

To create an instance, we call the class name followed by parentheses `()`.

We now have a unique `smeg` microwave object. If we try to `print` this object, Python tells us that we have a `Microwave` object at a unique memory address, confirming it's a specific, tangible thing built from our plan.

### 3. Adding Custom Details with the `__init__` Method

Our current microwave is just an empty shell. To make it useful, we need to give it specific details, like a brand name and a power rating. We can customize each new microwave as it's being created using a special method called `__init__`.

Methods that start and end with double underscores (`__`) are called "Dunder" methods in Python. The `__init__` method is the **initializer**; it runs automatically every time a new instance is created from the class, allowing us to set up its initial data. The `: str` part in the code below is an optional type hint, used for clarity to indicate that `brand` and `power_rating` are expected to be strings.

#### What is `self`?

You'll notice the `self` parameter in the `__init__` method. This is one of the most important concepts in classes.

`self` refers to the **actual instance of the class** that is being created or used. It’s the mechanism that ensures an object's data sticks to that specific object and doesn't get mixed up with others.

`"self is the actual instance of the class and that just makes sure that all this data sticks to the correct instance"`

It's a powerful "Aha!" moment for many learners to realize that `self` is just a strong convention, not a required keyword. You could technically name it `this`, `instance`, or even `s`, and the code would work. However, the Python community universally uses `self`, so you should always stick with that convention.

• When we create `smeg = Microwave("Smeg", "B")`, `self` inside `__init__` refers to the `smeg` object.

• When we create `bosch = Microwave("Bosch", "C")`, `self` refers to the `bosch` object.

This allows us to create multiple, distinct microwaves from the same blueprint, each with its own unique attributes.

Here is a clear comparison of our two unique microwave instances:

Instance

`brand` Attribute

`power_rating` Attribute

`smeg`

"Smeg"

"B"

`bosch`

"Bosch"

"C"

Now that our microwaves have data (attributes), it's time to give them actions (methods).

### 4. Making the Microwave Work: Adding Methods

**Methods** are functions defined inside a class that give an object its behavior. Our microwave needs to do things like turn on, turn off, and run. To manage this, we first need to track its current state. Let's add a `turned_on` attribute to our initializer, setting it to `False` by default. After all, as the source analogy notes, "imagine you open a box with a microwave and it's already turned on that would be kind of weird."

Here is our updated class, focusing only on the new attribute and methods:

The `turn_on` method includes a simple safety check:

1. It first checks the current state: `if self.turned_on`.

2. If the microwave is already on, it prints a message to inform the user.

3. If it's off, it changes the state (`self.turned_on = True`) and confirms the action was successful.

Let's test the full functionality of our `smeg` microwave:

This sequence produces the following output, showing how the object manages its own state:

Our methods work perfectly on one object. But the true advantage of classes emerges when we realize this functionality is reusable for any microwave we create.

### 5. The Real Power of Classes: Reusability

Why go through the effort of building a class? Because classes are the ultimate tool for organizing and reusing code. By bundling data (attributes) and functionality (methods) together into a single blueprint, we create a self-contained, reusable component.

This powerful workflow can be summarized in three steps:

1. **Define Once:** We designed the complete `Microwave` blueprint a single time.

2. **Create Many:** We can now instantly manufacture any number of unique microwaves from this blueprint—a `Smeg`, a `Bosch`, a `Samsung`, and more.

3. **Use Instantly:** Each new microwave we create works "straight out of the box." It automatically has all the defined attributes and methods, requiring no extra setup.

`"all the functionality is coupled with the class so you will have everything you need in one place and that just makes it easy to create functionality that actually works with minimal effort"`

Without a class, managing the state and functions for multiple microwaves would be complex and repetitive. With our class, it's effortless.

Now, let's explore one final topic: giving our custom objects the ability to interact with Python's built-in features.

### 6. A Touch of Magic: Understanding Dunder Methods

Dunder (double underscore) methods, sometimes called "magic methods," are special methods that allow our custom objects to work with Python's native syntax and functions. For example, what should happen if we try to add two microwaves together with the `+` operator?

**Output:**

Python raises a `TypeError` because it has no built-in rule for adding two `Microwave` objects. We can define this rule ourselves by implementing the `__add__` dunder method inside our class.

You aren't limited to returning strings; this method could perform a more complex operation and even return a new `Microwave` instance. The same pattern applies to other operators, like `*`, which can be defined with the `__mul__` method.

While you can define behavior for many operators, two of the most practical dunder methods for beginners are `__str__` and `__repr__`. These control how your object is represented as a string.

Dunder Method

Purpose

Intended Audience

Example Output

`__str__`

To provide a user-friendly, readable string representation.

The end-user (your "grandmother").

`Smeg (Rating: B)`

`__repr__`

To provide an unambiguous, developer-focused string representation that, ideally, could be used to recreate the object.

The developer.

`Microwave(brand='Smeg', power_rating='B')`

The `print()` function will automatically use the `__str__` method if it's available. If `__str__` is not defined, Python falls back to using `__repr__` instead. Defining these makes your objects much easier to inspect and debug.

### 7. Conclusion: You've Built Your First Class!

Congratulations! You have successfully designed and built a virtual microwave. We started with an empty `Microwave` blueprint and progressively added:

• **Attributes** (`brand`, `power_rating`) to store data.

• An **initializer** (`__init__`) to customize each new object.

• **Methods** (`turn_on`, `run`) to give our objects behavior.

• **Dunder methods** (`__str__`) to make our objects integrate cleanly with Python.

At its core, a class is simply a powerful and convenient way to create reusable blueprints for the objects in your code. By mastering classes, you unlock a more organized, scalable, and efficient way to build software. Happy coding!
