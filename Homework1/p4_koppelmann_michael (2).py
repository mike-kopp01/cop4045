# Michael Koppelmann Z23649817

from __future__ import annotations 

import os
import shutil
import tempfile

ENCODING = "utf-8"

def _check_str(value: str, name: str) -> None:
    """Check if a value is a string, raise TypeError if not."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string, got {type(value).__name__}")

def _check_int(value: object, name: str) -> None:
    """Check if a value is an integer, raise TypeError if not."""
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}")

def _load(filename: str) -> str:
    """Load the content of a file and return it as a string."""
    _check_str(filename, "filename")
    with open(filename, "r", encoding=ENCODING, newline="") as f:
        return f.read()

def _save(filename: str, content: str) -> None:
    """Save the content to a file, replacing its content."""
    folder = os.path.dirname(filename)
    fd, temp_path = tempfile.mkstemp(dir=folder, prefix=".ed_", suffix=".tmp")
    replace = False
    try:
        with os.fdopen(fd, "w", encoding=ENCODING, newline="") as f:
            f.write(content)
        replace = True
    finally:
        if replace:
            shutil.move(temp_path, filename)
        else:
            os.remove(temp_path)

def _positions(text: str, substring: str) -> list[int]:
    """Return a list of starting indices where substring occurs in text."""
    _check_str(text, "text")
    _check_str(substring, "substring")
    positions = []
    start = 0
    while True:
        start = text.find(substring, start)
        if start == -1:
            break
        positions.append(start)
        start += len(substring)
    return positions

def ed_read(filename: str, from_: int = 0, to: int = -1) -> str:
    """Read a portion of a file and return it as a string."""
    _check_str(filename, "filename")
    _check_int(from_, "from_")
    _check_int(to, "to")
    text = _load(filename)
    length = len(text)
    if not 0 <= from_ <= length:
        raise IndexError(f"from_ index {from_} outside the file " f"(length: {length})")
    if to == -1:
        to = length
    elif to < -1 or to > length:
        raise IndexError(f"to index {to} outside the file " f"(length: {length})")
    elif to < from_:
        raise ValueError(f"to index {to} is less than from_ index {from_}")
    return text[from_:to]

def ed_find(filename: str, search_str: str) -> list[int]:
    """Find all occurrences of search_str in a file and return their starting indices."""
    _check_str(filename, "filename")
    _check_str(search_str, "search_str")
    if search_str == "":
        raise ValueError("search_str must not be empty")
    text = _load(filename)
    return _positions(text, search_str)

def ed_replace(filename: str, search_str: str, replace_with: str, occurrence: int = -1) -> int:
    """Replace occurrences of search_str in a file with replace_with."""
    _check_str(filename, "filename")
    _check_str(search_str, "search_str")
    _check_str(replace_with, "replace_with")
    _check_int(occurrence, "occurrence")
    if search_str == "":
        raise ValueError("search_str must not be empty")
    if occurrence < -1:
        raise ValueError(f"occurrence must be -1 or >= 0, got {occurrence}")

    text = _load(filename)
    positions = _positions(text, search_str)
    if occurrence == -1:
        count = len(positions)
        new_text = text.replace(search_str, replace_with)
    elif occurrence < len(positions):
        count = 1
        start = positions[occurrence]
        new_text = text[:start] + replace_with + text[start + len(search_str):]
    else:
        count = 0

    if count > 0:
        _save(filename, new_text)
    return count

def ed_append(filename: str, string: str) -> int:
    """Append a string to the end of a file and return the number of characters written."""
    _check_str(filename, "filename")
    _check_str(string, "string")
    with open(filename, "a", encoding=ENCODING, newline="") as f:
        return f.write(string)

def testif(b: bool, tetsname: str, msgOK: str = "", MSGFailed: str = "") -> bool:
    """Test a boolean value and print a message."""
    if b:
        if msgOK:
            print(f"Test {tetsname} passed: {msgOK}")
        return True
    else:
        if MSGFailed:
            print(f"Test {tetsname} failed: {MSGFailed}")
        return b

def _write_fresh(filename: str, content: str) -> None:
    """Write content to a file, replacing its content."""
    _check_str(filename, "filename")
    _check_str(content, "content")
    with open(filename, "w", encoding=ENCODING, newline="") as f:
        f.write(content)

def test_ed_find() -> None:
    """Unit tests for ed_find(), using a temporary folder."""
    with tempfile.TemporaryDirectory() as folder:
        fn = os.path.join(folder, "find.txt")
        _write_fresh(fn, "01234567890123456789")

        testif(ed_find(fn, "345") == [3, 13], "ed_find two matches")
        testif(ed_find(fn, "356") == [], "ed_find no match")
        testif(ed_find(fn, "0") == [0, 10], "ed_find single char")
        testif(ed_find(fn, "01234567890123456789") == [0],
               "ed_find whole file")
        testif(ed_find(fn, "0123456789012345678901") == [],
               "ed_find longer than file")

        _write_fresh(fn, "aaaa")
        testif(ed_find(fn, "aa") == [0, 2], "ed_find non-overlapping matches")

        _write_fresh(fn, "")
        testif(ed_find(fn, "x") == [], "ed_find empty file")

        _write_fresh(fn, "héllo wörld héllo")
        testif(ed_find(fn, "héllo") == [0, 12], "ed_find non-ASCII text")

        try:
            ed_find(fn, "")
            testif(False, "ed_find empty search_str", "",
                   "no ValueError raised")
        except ValueError:
            testif(True, "ed_find empty search_str", "raised ValueError")

        try:
            ed_find(fn, 5)
            testif(False, "ed_find non-str search_str", "",
                   "no TypeError raised")
        except TypeError:
            testif(True, "ed_find non-str search_str", "raised TypeError")

        try:
            ed_find(os.path.join(folder, "missing.txt"), "x")
            testif(False, "ed_find missing file", "",
                   "no FileNotFoundError raised")
        except FileNotFoundError:
            testif(True, "ed_find missing file",
                   "FileNotFoundError passed to caller")


def test_ed_replace() -> None:
    """Unit tests for ed_replace(), using a temporary folder."""
    start = "01234567890123456789"
    with tempfile.TemporaryDirectory() as folder:
        fn = os.path.join(folder, "replace.txt")

        _write_fresh(fn, start)
        n = ed_replace(fn, "345", "ABCDE", 1)
        testif(n == 1 and _load(fn) == "0123456789012ABCDE6789",
               "ed_replace second occurrence", _load(fn), _load(fn))

        _write_fresh(fn, start)
        n = ed_replace(fn, "345", "ABCDE")
        testif(n == 2 and _load(fn) == "012ABCDE6789012ABCDE6789",
               "ed_replace all occurrences", _load(fn), _load(fn))

        _write_fresh(fn, start)
        n = ed_replace(fn, "345", "X", 0)
        testif(n == 1 and _load(fn) == "012X67890123456789",
               "ed_replace first occurrence")

        _write_fresh(fn, start)
        n = ed_replace(fn, "345", "X", 2)
        testif(n == 0 and _load(fn) == start,
               "ed_replace occurrence too large",
               "no change", "file was changed")

        _write_fresh(fn, start)
        n = ed_replace(fn, "xyz", "Q")
        testif(n == 0 and _load(fn) == start, "ed_replace not found")

        _write_fresh(fn, start)
        n = ed_replace(fn, "345", "")
        testif(n == 2 and _load(fn) == "01267890126789",
               "ed_replace with empty string")

        _write_fresh(fn, "aaaa")
        n = ed_replace(fn, "aa", "b")
        testif(n == 2 and _load(fn) == "bb",
               "ed_replace count matches ed_find")

        _write_fresh(fn, "line1\r\nline2\r\n")
        n = ed_replace(fn, "line2", "LINE2")
        testif(n == 1 and _load(fn) == "line1\r\nLINE2\r\n",
               "ed_replace keeps line endings")

        for label, args, exc in [
                ("empty search_str", ("", "x"), ValueError),
                ("occurrence < -1", ("345", "x", -2), ValueError),
                ("non-str replace_with", ("345", 7), TypeError),
                ("non-int occurrence", ("345", "x", "1"), TypeError)]:
            _write_fresh(fn, start)
            try:
                ed_replace(fn, *args)
                testif(False, "ed_replace " + label, "",
                       f"no {exc.__name__} raised")
            except exc:
                testif(_load(fn) == start, "ed_replace " + label,
                       f"raised {exc.__name__}, file unchanged",
                       "file was changed")

        try:
            ed_replace(os.path.join(folder, "missing.txt"), "a", "b")
            testif(False, "ed_replace missing file", "",
                   "no FileNotFoundError raised")
        except FileNotFoundError:
            testif(True, "ed_replace missing file",
                   "FileNotFoundError passed to caller")



def main() -> None:
    """Demo all ed_ functions, then run the unit tests."""
    with tempfile.TemporaryDirectory() as folder:
        fn = os.path.join(folder, "file1.txt")

        print("ed_append returns", ed_append(fn, "0123456789"))
        print("ed_append returns", ed_append(fn, "0123456789"))
        print("file content:      ", ed_read(fn))
        print("ed_read(fn, 3, 9): ", ed_read(fn, 3, 9))
        print("ed_read(fn, 3):    ", ed_read(fn, 3))
        print('ed_find(fn, "345"):', ed_find(fn, "345"))
        print('ed_find(fn, "356"):', ed_find(fn, "356"))

        n = ed_replace(fn, "345", "ABCDE", 1)
        print(f'ed_replace(fn, "345", "ABCDE", 1) -> {n}; file: {ed_read(fn)}')

        _write_fresh(fn, "01234567890123456789")
        n = ed_replace(fn, "345", "ABCDE")
        print(f'ed_replace(fn, "345", "ABCDE")    -> {n}; file: {ed_read(fn)}')

        try:
            ed_read(fn, 0, 1000)
        except IndexError as e:
            print("IndexError:", e)
        try:
            ed_read(os.path.join(folder, "nope.txt"))
        except FileNotFoundError as e:
            print("FileNotFoundError:", e.strerror)

    print("\n--- test_ed_find ---")
    test_ed_find()
    print("\n--- test_ed_replace ---")
    test_ed_replace()


if __name__ == "__main__":
    main()
