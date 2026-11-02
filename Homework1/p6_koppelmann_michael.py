# Michael Koppelmann Z23649817

from __future__ import annotations 

import math
import unittest
from numbers import Real
from typing import Optional 

class Entry: 
    """Base class for files and folders in a hierarchical tree."""
    
    def __init__(self, name: str, parent: Optional[Folder] = None) -> None: 
        """Create a named entry and optionally add it to a parent folder."""
        if not isinstance(name, str):
           raise TypeError("name must be a str")
        if not name:
            raise ValueError("name must not be empty")
        self.name: str = name
        self._parent: Optional[Folder] = None
        if parent is not None:
            if not isinstance(parent, Folder):
                raise TypeError("parent must be a Folder or None")
            parent.add(self)

    def parent(self) -> Optional[Folder]:
        """Return this entry's parent folder, or None if it is a root."""
        return self._parent

    def size(self) -> int:
        """Return the entry's size in bytes; subclasses must implement this."""
        raise NotImplementedError("subclasses of Entry must override size()")

    def absolute_path(self) -> list[Entry]:
        """Return this entry and its ancestors, starting with this entry."""
        if self._parent is None:
            return [self]
        return [self] + self._parent.absolute_path()

    def path_str(self) -> str:
        """Return the entry's absolute path as a slash-separated string."""
        return "/" + "/".join(e.name for e in reversed(self.absolute_path()))

    def __str__(self) -> str:
        """Return the entry's name."""
        return self.name

    def __repr__(self) -> str:
        """Return a concise representation containing the type and name."""
        return f"{type(self).__name__}({self.name!r})"


class File(Entry):
    """A file with a fixed size in bytes."""

    def __init__(self, name: str, bytes_used: int,
                 parent: Optional[Folder] = None) -> None:
        """Create a file and optionally place it in a parent folder."""
        if isinstance(bytes_used, bool) or not isinstance(bytes_used, int):
            raise TypeError("bytes_used must be an int")
        if bytes_used < 0:
            raise ValueError("bytes_used must be non-negative")
        self.bytes_used: int = bytes_used
        super().__init__(name, parent)

    def size(self) -> int:
        """Return the file's size in bytes."""
        return self.bytes_used

    def __repr__(self) -> str:
        """Return a short description like File('a.txt', 100)."""
        return f"File({self.name!r}, {self.bytes_used})"


class Folder(Entry):
    """A directory containing child files and folders."""

    def __init__(self, name: str, parent: Optional[Folder] = None) -> None:
        """Create an empty folder and optionally place it in a parent."""
        self._children: list[Entry] = []
        super().__init__(name, parent)

    def add(self, entry: Entry) -> None:
        """Add an unparented entry, rejecting invalid entries and cycles."""
        if not isinstance(entry, Entry):
            raise TypeError("only Entry objects can be added to a Folder")
        if entry is self:
            raise ValueError(f"adding {entry.name!r} to {self.name!r} "
                             "would create a cycle")
        if entry.parent() is not None:
            raise ValueError(f"{entry.name!r} is already in folder "
                             f"{entry.parent().name!r}")
        if any(e is entry for e in self.absolute_path()):
            raise ValueError(f"adding {entry.name!r} to {self.name!r} "
                             "would create a cycle")
        self._children.append(entry)
        entry._parent = self

    def children(self) -> tuple[Entry, ...]:
        """Return this folder's children as an immutable tuple."""
        return tuple(self._children)

    def size(self) -> int:
        """Return the total size of all files contained in this folder."""
        return sum(child.size() for child in self._children)


def find_large_files(entry: Entry, minimum_size: Real) -> list[File]:
    """Find files at least minimum_size bytes within an entry's subtree."""
    if isinstance(minimum_size, bool) or not isinstance(minimum_size, Real):
        raise TypeError("minimum_size must be a number")
    minimum_size = float(minimum_size)
    if not math.isfinite(minimum_size):
        raise ValueError("minimum_size must be finite")
    if minimum_size < 0:
        raise ValueError("minimum_size must be non-negative")

    if isinstance(entry, File):
        return [entry] if entry.size() >= minimum_size else []
    if isinstance(entry, Folder):
        result: list[File] = []
        for child in entry.children():
            result += find_large_files(child, minimum_size)
        return result
    raise TypeError("entry must be a File or a Folder")


def build_sample_tree() -> Folder:
    """Build and return a sample university folder tree."""
    root = Folder("university")
    File("readme.txt", 2_000, root)
    courses = Folder("courses", root)
    File("syllabus.pdf", 350_000, courses)
    cop = Folder("cop4045", courses)
    File("notes.txt", 12_000, cop)
    lectures = Folder("lectures", cop)
    File("lecture01.mp4", 250_000_000, lectures)
    File("slides01.pdf", 3_500_000, lectures)
    Folder("empty", cop)
    photos = Folder("photos", root)
    File("campus.jpg", 4_500_000, photos)
    return root


def _print_tree(entry: Entry, indent: int = 0) -> None:
    """Print an entry and its descendants as an indented tree."""
    label = entry.name + ("/" if isinstance(entry, Folder) else "")
    width = 30 - 4 * indent
    print(f"{'    ' * indent}{label:<{width}} {entry.size():>13,} bytes")
    if isinstance(entry, Folder):
        for child in entry.children():
            _print_tree(child, indent + 1)


class EntryTests(unittest.TestCase):
    """Unit tests for Entry, File, Folder, and find_large_files()."""

    def setUp(self) -> None:
        self.root = Folder("root")
        self.a = File("a.txt", 100, self.root)
        self.sub = Folder("sub", self.root)
        self.b = File("b.bin", 5000, self.sub)
        self.deep = Folder("deep", self.sub)
        self.c = File("c.log", 50, self.deep)
        self.d = File("d.dat", 5000, self.deep)
        self.empty = Folder("empty", self.root)

    def test_absolute_path(self) -> None:
        self.assertEqual(self.root.absolute_path(), [self.root])
        self.assertEqual(self.a.absolute_path(), [self.a, self.root])
        self.assertEqual(
            self.d.absolute_path(),
            [self.d, self.deep, self.sub, self.root],
        )

    def test_path_str(self) -> None:
        self.assertEqual(self.root.path_str(), "/root")
        self.assertEqual(self.d.path_str(), "/root/sub/deep/d.dat")

    def test_folder_size_and_children(self) -> None:
        self.assertEqual(self.root.size(), 100 + 5000 + 50 + 5000)
        self.assertEqual(self.deep.size(), 5050)
        self.assertEqual(self.empty.size(), 0)
        self.assertIsInstance(self.root.children(), tuple)

    def test_find_large_files(self) -> None:
        self.assertEqual(find_large_files(self.root, 5000), [self.b, self.d])
        self.assertEqual(find_large_files(self.root, 0), [self.a, self.b, self.c, self.d])
        self.assertEqual(find_large_files(self.root, 5001), [])
        self.assertEqual(find_large_files(self.empty, 0), [])

    def test_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            find_large_files(self.root, -1)
        with self.assertRaises(TypeError):
            find_large_files(self.root, "10")
        with self.assertRaises(TypeError):
            find_large_files("root", 10)


def main() -> None:
    """Demonstrate tree sizes, polymorphism, paths, and large-file searches."""
    root = build_sample_tree()
    print("Sample folder tree:")
    _print_tree(root)

    print(f"\nroot.size() = {root.size():,} bytes")
    print("\nPolymorphism: the same size() call on mixed entries:")
    for entry in root.children():
        kind = type(entry).__name__
        print(f"  {kind:<6} {entry.name:<12} size() = {entry.size():,}")

    for threshold in (1_000_000, 10_000):
        large = find_large_files(root, threshold)
        print(f"\nfind_large_files(root, {threshold:,}) -> "
              f"{len(large)} files:")
        for f in large:
            print(f"  {f.path_str():<52} {f.size():>13,}")

    readme = root.children()[0]
    small = find_large_files(readme, 1_000)
    print(f"\nfind_large_files(readme.txt, 1,000)     -> {small}")
    none = find_large_files(readme, 1_000_000)
    print(f"find_large_files(readme.txt, 1,000,000) -> {none}")

    lecture = find_large_files(root, 100_000_000)[0]
    print("\nabsolute_path() of lecture01.mp4:")
    print("  ", lecture.absolute_path())
    print("   names:", " -> ".join(e.name for e in lecture.absolute_path()))
    print("   as a path:", lecture.path_str())
    print("absolute_path() of the root:", root.absolute_path())


if __name__ == "__main__":
    main()
