# Michael Koppelmann Z23649817
from __future__ import annotations 

from numbers import Real
from typing import Any, Union

Number = Union[int, float]
total_tests = 0
passed_tests = 0

def testif(b: bool, testname: str, msgOK: str= "", msgFailed: str= "") -> bool:
    """Test a boolean value and print a message."""
    """Postcondition: Increments the global total_tests counter. 
    If b is True, increments the global passed_tests counter and prints a message indicating that the test passed. 
    If b is False, prints a message indicating that the test failed."""
    """Precondition: b is a boolean value, testname is a string, msgOK and msgFailed are optional strings."""
    """Raises: None"""
    """Parameters: b - A boolean value to test, testname - A string representing the name of the test, msgOK - An optional string representing the message to print if the test passes, msgFailed - An optional string representing the message to print if the test fails."""
    global total_tests, passed_tests

    total_tests += 1

    if b:
        passed_tests += 1
        print(f"PASS {total_tests}: {testname}", flush=True)
    else:
        print(f"FAIL {total_tests}: {testname}", flush=True)

    return b

class NVector:
    """A class representing a vector of numbers."""
    """Invariant: All elements of the vector are real numbers (int or float)."""
    def __init__(self, *args: Any) -> None:
        """Initialize an NVector instance."""
        """Usage: NVector(1, 2, 3) or NVector([1, 2, 3]) or NVector((1, 2, 3))"""
        """Precondition: All arguments must be real numbers (int or float)."""
        """Postcondition: Creates an NVector instance with the specified elements."""
        """Raises TypeError if any argument is not a real number."""
        """Parameters: *args - A variable number of arguments representing the elements of the vector."""
        if len(args) == 1:
            elems = list(args[0])
        else: 
            elems = list(args)
        for e in elems:
            NVector._check_number(e)
        self._elems = elems

    @staticmethod
    def _check_number(value: Any) -> None:
        """Check if the value is a real number (int or float)."""
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError(f"NVector elements must be a real numbers, got {value!r}")

    @staticmethod
    def _check_index(index: Any) -> None:
        """Check if the index is an integer."""
        if isinstance(index, bool) or not isinstance(index, int):
            raise TypeError(f"NVector index must be an integer, not {index!r}" f"{type(index).__name__}")

    @classmethod
    def zeros(cls, n: int) -> NVector:
        """Create an NVector of length n filled with zeros."""
        if isinstance(n , bool) or not isinstance(n, int): 
            raise TypeError("dimensions must be an int, not " f"{type(n).__name__}")
        if n < 0:
            raise ValueError(f"dimensions must be non-negative, got {n}")
        return cls([0] * n)

    def __len__(self) -> int:
        """Return the length of the NVector."""
        return len(self._elems)

    def __getitem__(self, index: int) -> Number:
        """Return the element at the specified index."""
        NVector._check_index(index)
        return self._elems[index]

    def __setitem__(self, index: int, value: Number) -> None:
        """Set the element at the specified index to the given value."""
        NVector._check_index(index)
        NVector._check_number(value)
        self._elems[index] = value

    def __str__(self) -> str:
        """Return a string representation of the NVector."""
        return "[" + ", ".join(str(e) for e in self._elems) + "]"

    def __repr__(self) -> str:
        """Return a string representation of the NVector for debugging."""
        return f"NVector({self._elems!r})"

    def __eq__(self, other: object) -> bool:
        """Check if two NVectors are equal."""
        if not isinstance(other, NVector):
            return False
        return self._elems == other._elems

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: Union[NVector, Number]) -> NVector:
        """Add two NVectors or an NVector and a number."""
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Cannot add NVector of different lengths")
            return NVector([a + b for a, b in zip(self._elems, other._elems)])
        elif isinstance(other, Real) and not isinstance(other, bool):
            return NVector([a + other for a in self._elems])
        else:
            return NotImplemented

    def __radd__(self, other: Number) -> NVector:
        """Add a number and an NVector."""
        return self.__add__(other)

    def __mul__(self, other: Union[NVector, Number]) -> Number:
        """Multiply two NVectors (dot product) or an NVector and a number."""
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Cannot multiply NVector of different lengths")
            return sum(a * b for a, b in zip(self._elems, other._elems))
        elif isinstance(other, (int, float)):
            return sum(a * other for a in self._elems)
        else:
            return NotImplemented

    def __rmul__(self, other: Number) -> Number:
        """Multiply a number and an NVector."""
        return self.__mul__(other)

def main() -> None:
    """Run tests for the NVector class."""
    """Postcondition: Prints the results of the tests and a summary of the total tests, passed tests, and failed tests."""
    """Precondition: None"""
    """Raises: None"""
    """Parameters: None"""
    global total_tests, passed_tests
    total_tests = 0
    passed_tests = 0
    lst = [3, 0, 1, -1]
    v = NVector(lst)
    testif(v == NVector(3, 0, 1, -1), "constructor from list")
    testif(NVector((3, 0, 1, -1)) == v, "constructor from tuple")
    lst[0] = 100
    testif(v[0] == 3, "constructor copies the list", "list not shared",
           "list is shared with the argument")
    try:
        NVector(5)
        testif(False, "constructor with scalar", "", "no TypeError raised")
    except TypeError:
        testif(True, "constructor with scalar", "raised TypeError")
    try:
        NVector([1, "a", 3])
        testif(False, "constructor with non-number", "", "no TypeError raised")
    except TypeError:
        testif(True, "constructor with non-number", "raised TypeError")

    v = NVector(3, 0, 1, -1)
    testif(len(v) == 4 and v[0] == 3 and v[3] == -1, "constructor with 4 args")
    testif(NVector(1, 2) == NVector([1, 2]), "constructor with 2 args")

    testif(len(NVector([3, 0, 1, -1])) == 4, "len works", "len is 4",
           "len is wrong")
    testif(len(NVector([])) == 0, "len of empty vector")

    x = NVector([3, 0, 1, -1])
    testif(x[1] == 0, "getitem positive index")
    testif(x[-2] == 1, "getitem negative index")
    try:
        x[4]
        testif(False, "getitem out of range", "", "no IndexError raised")
    except IndexError:
        testif(True, "getitem out of range", "raised IndexError")
    try:
        x["1"]
        testif(False, "getitem non-int index", "", "no TypeError raised")
    except TypeError:
        testif(True, "getitem non-int index", "raised TypeError")

    v = NVector(1, 2, 3, 4)
    v[3] = 10
    testif(v[3] == 10, "setitem", "setitem works", "setitem failed")
    x = NVector([3, 0, 1, -1])
    x[2] = 5
    testif(x == NVector([3, 0, 5, -1]), "setitem example from spec")
    x[-1] = 7
    testif(x[3] == 7, "setitem negative index")
    try:
        x[10] = 1
        testif(False, "setitem out of range", "", "no IndexError raised")
    except IndexError:
        testif(True, "setitem out of range", "raised IndexError")
    try:
        x[0] = "hi"
        testif(False, "setitem non-number value", "", "no TypeError raised")
    except TypeError:
        testif(True, "setitem non-number value", "raised TypeError")

    testif(str(NVector(3, 0, 1, -1)) == "[3, 0, 1, -1]", "str works",
           str(NVector(3, 0, 1, -1)))
    testif(str(NVector([])) == "[]", "str of empty vector")

    a = NVector(1, 2, 3)
    testif(a == NVector([1, 2, 3]), "eq on equal vectors")
    testif(not (a == NVector(1, 2, 4)), "eq on different elements")
    testif(not (a == NVector(1, 2)), "eq on different lengths")
    testif(not (a == [1, 2, 3]), "eq with a list is False")
    testif(a != NVector(1, 2, 4), "ne on different vectors")
    testif(not (a != NVector(1, 2, 3)), "ne on equal vectors")
    testif(a != "abc", "ne with a non-NVector is True")

    v = NVector([3, 0, 1, -1])
    testif(v + NVector([1, 2, 3, 4]) == NVector([4, 2, 4, 3]),
           "add two vectors")
    testif(v + 10 == NVector([13, 10, 11, 9]), "add vector + number")
    testif(10 + v == NVector([13, 10, 11, 9]), "radd number + vector")
    testif(v == NVector([3, 0, 1, -1]), "add does not modify operand")
    try:
        v + NVector(1, 2)
        testif(False, "add different lengths", "", "no ValueError raised")
    except ValueError:
        testif(True, "add different lengths", "raised ValueError")
    try:
        v + "x"
        testif(False, "add with a string", "", "no TypeError raised")
    except TypeError:
        testif(True, "add with a string", "raised TypeError")

    testif(v * NVector([1, 2, 3, 4]) == 2, "mul dot product")
    testif(v * 2 == 6, "mul vector * number", "sum of Ai*2 == 6")
    testif(2 * v == 6, "rmul number * vector")
    try:
        v * NVector(1, 2)
        testif(False, "mul different lengths", "", "no ValueError raised")
    except ValueError:
        testif(True, "mul different lengths", "raised ValueError")
    try:
        v * "x"
        testif(False, "mul with a string", "", "no TypeError raised")
    except TypeError:
        testif(True, "mul with a string", "raised TypeError")

    z = NVector.zeros(3)
    testif(z == NVector(0, 0, 0), "zeros(3)")
    testif(len(NVector.zeros(0)) == 0, "zeros(0)")
    try:
        NVector.zeros(-1)
        testif(False, "zeros negative", "", "no ValueError raised")
    except ValueError:
        testif(True, "zeros negative", "raised ValueError")

    print("\n====== TEST SUMMARY ======")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print("===========================")

if __name__ == "__main__":
    main()
