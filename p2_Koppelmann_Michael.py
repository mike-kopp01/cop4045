# Michael Koppelmann Problem 2 Homework 1
# This is my Pythagorean formula that uses range for a, b, c to find the triples within the numbers provided
def find_Pythagorean(n):
    triples = []
    for a in range(1, n + 1):
        for b in range(a, n + 1):
            for c in range(a, n + 1):
                if a * a + b * b == c * c:
                    triples.append((a, b, c))
    return triples

# Asking for a positive number to make the formula work but also easier
n = int (input("Enter a positive integer to continue: "))
result = find_Pythagorean(n)

# Printing the results from the formula and the total using len
print(f"The Pythagorean triples for {n} are: ")
for a, b, c in result: 
    print(f"{a}, {b}, {c}")
    print(f"Total from the Pythagorean formula: {len(result)}")

