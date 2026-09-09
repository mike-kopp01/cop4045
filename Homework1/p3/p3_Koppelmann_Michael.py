# Michael Koppelmann Problem 3 Homework
# First part of the code for the duplicated strings
def dup_str(s, n):
    if n <= 0 or n > len(s):
        return ""
    # Looks for the duplicated string in the given input
    for i in range(len(s) - n + 1):
        sub = s[i:i + n]
        if sub in s[i + 1:]:
            return sub
    return ""

# Defines what the max duplicated string function is
def max_dup(s):
    # Looks for the max duplicated string from the input
    for n in range(len(s) - 1, 0, -1):
        result = dup_str(s, n)
        if result:
            return result
    return ""

# This is getting the input from the user to input the data
def main():
    # User input of the string and the length
    s = input("Please enter a string: ")
    n = int(input("Please enter a substring length: "))
    result = dup_str(s, n)
    # Gives the duplicated string and also gives an answer if there is no duplicated string found
    if result:
        print(f"The first duplicated substring of a length {n}: {result}")
    else:
        print(f"There is no duplicated substring of length {n}.")
    # This gives the longest string from the duplicated string and also an answer for zero duplicated string
    longest = max_dup(s)
    if longest:
        print(f"This is the longest duplicated substring: {longest}")
    else:
        print(f"There is no duplicated longest substring.")

if __name__ == "__main__":
    main()