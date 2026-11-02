# Michael Koppelmann Z23649817

from __future__ import annotations 

import math
import time
import turtle 
from typing import Any, Optional, Sequence 

def testif(b: bool, testname: str, msgOK: str = "", magFailed: str= "") -> bool:
    """Test a boolean value and print a message.

    Args:
        b: The boolean value to test.
        testname: The name of the test.
        msgOK: The message to print if the test passes.
        magFailed: The message to print if the test fails."""
    
    if b:
        print(f"Test {testname} passed. {msgOK}")
    else:
        print(f"Test {testname} failed. {magFailed}")
    return b

SIDE_ANGLE = 45
SIDE_RATIO = 0.42
TOP_RATIO = 0.72

def _start_drawing(x: float, y: float) -> None:
    """Move the turtle to the starting position and set the heading.

    Args:
        x: The x-coordinate of the starting position.
        y: The y-coordinate of the starting position."""
    
    turtle.penup()
    turtle.setpos(x, y)
    turtle.setheading(90)
    turtle.pendown()

def _leaf_straight(level: int, length: float) -> None:
    """Draw a straight leaf.

    Args:
        level: The level of recursion.
        length: The length of the leaf."""
    
    turtle.forward(length)
    if level > 0:
        turtle.left(SIDE_ANGLE)
        _leaf_straight(level - 1, length * SIDE_RATIO)
        turtle.right(2 * SIDE_ANGLE)
        _leaf_straight(level - 1, length * SIDE_RATIO)
        turtle.left(SIDE_ANGLE)
        _leaf_straight(level - 1, length * TOP_RATIO)
    turtle.backward(length)

def draw_leaf_straight(level: int, length: float, x: float = 0, y: float = -300) -> None:
    """Draw a straight leaf at the specified position.

    Args:
        level: The level of recursion.
        length: The length of the leaf.
        x: The x-coordinate of the starting position.
        y: The y-coordinate of the starting position."""
    
    _check_leaf_args(level, length)
    _start_drawing(x, y)
    _leaf_straight(level, length)

CURVE_BEND = 9
CURVE_LEFT = 52
CURVE_RIGHT = 48
CURVE_LEFT_RATIO = 0.48
CURVE_RIGHT_RATIO = 0.40
CURVE_TOP_RATIO = 0.74

def _curved_stem(length: float, bend: float) -> None:
    radius = abs(length) / math.radians(bend)
    extent = bend if length > 0 else -bend
    turtle.circle(-radius, extent)

def _leaf_curved(level: int, length: float) -> None:
    """Draw a curved leaf.

    Args:
        level: The level of recursion.
        length: The length of the leaf."""
    
    _curved_stem(length, CURVE_BEND)
    if level > 0:
        turtle.left(CURVE_LEFT)
        _leaf_curved(level - 1, length * CURVE_LEFT_RATIO)
        turtle.right(CURVE_LEFT + CURVE_RIGHT)
        _leaf_curved(level - 1, length * CURVE_RIGHT_RATIO)
        turtle.left(CURVE_RIGHT)
        _leaf_curved(level - 1, length * CURVE_TOP_RATIO)
    _curved_stem(-length, CURVE_BEND)

def draw_leaf_curved(level: int, length: float, x: float = 0, y: float = -300) -> None:
    """Draw a curved leaf at the specified position.

    Args:
        level: The level of recursion.
        length: The length of the leaf.
        x: The x-coordinate of the starting position.
        y: The y-coordinate of the starting position."""
    
    _check_leaf_args(level, length)
    _start_drawing(x, y)
    turtle.forward(length * 0.6)
    _leaf_curved(level, length)
    turtle.backward(length * 0.6)

def _check_leaf_args(level: int, length: float) -> None:
    if isinstance(level, bool) or not isinstance(level, int):
        raise TypeError("level must be an int")
    if level < 0:
        raise ValueError("level must be >= 0")
    if length <= 0:
        raise ValueError("length must be > 0")

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def strB(n: int, base: int = 10) -> str:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int")
    if isinstance(base, bool) or not isinstance(base, int):
        raise TypeError("base must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")
    if not 2 <= base <= 26:
        raise ValueError("base must be between 2 and 26")

    if n < base:
        return DIGITS[n]
    return strB(n // base, base) + DIGITS[n % base]

def test_strB() -> None:
    testif(strB(0) == "0", "strB(0)")
    testif(strB(255, base=2) == "11111111", "strB(255, base=2)")
    testif(strB(48879, base=16) == "BEEF", "strB(48879, base=16)")
    testif(strB(675, base=26) == "PP", "strB(675, base=26)")

_cnk_memo : dict[tuple[int, int], int] = {}

def Cnk_m(n: int, k: int) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or \
            isinstance(k, bool) or not isinstance(k, int):
        raise TypeError("n and k must be ints")
    if not 0 <= k <= n:
        raise ValueError("need 0 <= k <= n")

    if k == 0 or k == n:
        return 1
    if (n, k) in _cnk_memo:
        return _cnk_memo[(n, k)]
    result = Cnk_m(n - 1, k - 1) + Cnk_m(n - 1, k)
    _cnk_memo[(n, k)] = result
    return result

def test_Cnk_m() -> None:
    testif(Cnk_m(5, 0) == 1, "Cnk_m(5, 0) base case")
    testif(Cnk_m(10, 3) == 120, "Cnk_m(10, 3) computed case")
    testif(Cnk_m(52, 5) == 2598960, "Cnk_m(52, 5) poker hands")
    testif(Cnk_m(100, 50) == 100891344545564193334812497256, "Cnk_m(100, 50) large case")

def run_Cnk() -> None:
    print(f"{'n':>4} {'k':>4}  {'time (ms)':>9}  ok  C(n, k)")
    for n, k in [(6, 3), (20, 10), (52, 5), (100, 50), (300, 150), (600, 300)]:
        _cnk_memo.clear()
        start = time.perf_counter()
        value = Cnk_m(n, k)
        ms = (time.perf_counter() - start) * 1000
        ok = value == math.comb(n, k)
        print(f"{n:>4} {k:>4}  {ms:9.3f}  {'Y' if ok else 'N':>2}  {value}")

def make_pairs(seq1: Sequence[Any], seq2: Sequence[Any], acc: Optional[list[tuple[Any, Any]]] = None, i: int = 0) -> list[tuple[Any, Any]]:
    if acc is None:
        acc = []
    if i >= len(seq1) or i >= len(seq2):
        return acc
    acc.append((seq1[i], seq2[i]))
    return make_pairs(seq1, seq2, acc, i + 1)

def test_make_pairs() -> None:
    testif(make_pairs([1, 2, 3], [4, 5, 6]) == [(1, 4), (2, 5), (3, 6)],
           "make_pairs equal lengths")
    testif(make_pairs([1, 2, 3], [4, 5]) == [(1, 4), (2, 5)],
           "make_pairs second list shorter")
    testif(make_pairs([1], [4, 5, 6, 7]) == [(1, 4)],
           "make_pairs first list has one element")
    testif(make_pairs([], [4, 5, 6]) == [], "make_pairs first list empty")
    testif(make_pairs([1, 2, 3], []) == [], "make_pairs second list empty")

def main() -> None:
    print("--- strB ---")
    test_strB()
    print("--- Cnk_m ---")
    test_Cnk_m()
    run_Cnk()
    print("--- make_pairs ---")
    test_make_pairs()

    turtle.setup(1100, 800)
    turtle.title("Recursive leaves")
    turtle.delay(0)
    turtle.tracer(0, 0)
    turtle.hideturtle()
    draw_leaf_straight(8, 120, x=-260, y=-330)
    draw_leaf_curved(8, 120, x=200, y=-330)
    turtle.update()
    turtle.done()

if __name__ == "__main__":
    main()
