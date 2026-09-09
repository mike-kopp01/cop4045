# Michael Koppelmann Problem 4 Homework 1
# Importing the math and graph function
import math 
import matplotlib.pyplot as plt

# This lays out the plot function and the x and y values with the max and min
def plot_function(func_str, ns, xmin, xmax):
    step = (xmax - xmin) / (ns - 1)
    xs = [xmin + i * step for i in range(ns)]
    ys = [eval(func_str, {"math": math, "__builtins__": {}}, {"x": x}) for x in xs]

    #This prints the table in the same format required for the assignment
    print(f"{'x':>10}{'y':>12}")
    print("-" * 22)
    for x, y in zip(xs, ys):
        print(f"{float(x):>10.4f}{float(y):>+12.4f}")

    # This prints the graph for the given table with a marker, markersize, and linewidth
    plt.plot(xs, ys, marker="o", markersize=4, linewidth=1)
    plt.title(func_str)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()

    return xs, ys

# This asks the user for the variable of x, positive samples, min, and max values
def main():
    func_str = input("Enter function with a variable of x: ")
    ns = int(input("Enter a number of positive samples: "))
    xmin = float(input("Enter min: "))
    xmax = float(input("Enter max: "))
    plot_function(func_str, ns, xmin, xmax)

if __name__ == "__main__":
    main()