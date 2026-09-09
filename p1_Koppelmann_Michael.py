# Michael Koppelmann Problem 1 Homework 1
# These are the first imports for the code with math, numpy, and matplot for the graph
import math
import numpy as np
import matplotlib.pyplot as plt

# The first function for the quadratic function creating the parameters a, b, c
def quadratic_function(a, b, c):
    function = b**2 - 4 * a * c

# These are the if statements to make sure it runs for greater than, less than, and equal to for one solution, two soltuions, and no solution
    # No Solutuioncondition
    if function < 0:
        print(f" Function = {function:.4g} -> No Real Solution!")
        number = []
    # One Solution condition
    elif function == 0:
        root = -b / (2 * a)
        print(f" Function = {function:.4g} -> One Real Solution!: x = {number:.4g}")
        numbers = [numbers]
    # Two Soltuions condition
    else:
        sqrt_d = math.sqrt(function)
        num1 = (-b + sqrt_d) / (2 * a)
        num2 = (-b - sqrt_d) / (2 * a)
        print(f" Function= {function:.4g} -> Two Real Solutions!: x1 = {num1:.4g}, x2 = {num2:.4g}")
        numbers = sorted([num1, num2])

    # Returns the number for the coffeicient and for graphing
    return number, function

# Sets the conditions for the domain for graphing the function
def domain(a, b, c, numbers, points=150):
        # Vertex of graph
        vertex_of_x = -b / (2 * a)
        # Creates a linespace if there are no numberes, if numbers exist it creates padding for the graph
        if not numbers:
          span = 5
          x = np.linspace(vertex_of_x - span, vertex_of_x + span, points)
        # Creates padding for the graph
        else:
            lo, hi = min(numbers), max(numbers)
            padding = max((hi - lo) * 0.5, 1)
            x = np.linspace(lo - padding, hi + padding, points)

        return x

# Plotting the quadratic function with a graph with numbers given by the user
def plot_quadratic(a, b, c, numbers):
    x = domain(a, b, c, numbers, points=150)
    y = a * x**2 + b * x + c
    # Conditions for the graph
    plt.figure(figsize=(7, 5))
    plt.plot(x, y, color="red", linewidth=3,
             label=f"y = {a}x^2 + {b}x + {c}")
    plt.axhline(0, color="black", linewidth=0.5)
    plt.axvline(0, color="gray", linewidth=0.5)
    # Numbers conditions of the graph
    if numbers:
        plt.scatter(numbers, [0] * len(numbers), color="blue", zorder=5,
                    label="Real Numbers(s)", s=65)
    # Title, legend, grid, and showing the graph
    plt.title(f"{a}x^2 = {b}x + {c} = 0")
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.show()

# This is the last function that runs getting inputs from the user to compute the code
def main():
    while True:
        user_input = input("Enter the variables a b c (press Enter to quit): ").strip()
        if user_input == "":
            print("Program terminated!")
            break
        try:
                a, b, c = map(float, user_input.split())
        except ValueError:
            print("Please continue to enter exactly three numbers, seperated by spaces.")
            continue
        if a == 0:
            print("'a' cannot be 0 (not a quatratic equation).")
            continue

        numbers, function = quadratic_function(a, b, c)
        plot_quadratic(a, b, c, numbers)

# Last part of the code to actually run it
if __name__ == "__main__":
    main()      
    