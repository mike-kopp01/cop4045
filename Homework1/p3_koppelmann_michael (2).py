# Michael Koppelmann Z23649817

from __future__ import annotations 

import random 
from typing import Optional, Union

import matplotlib.pyplot as plt

Cell = Union["Animal", int]
Location = tuple [int, int]

class Island(object):
    """A class representing an island with a grid of cells that can contain animals."""
    """Postcondition: Initializes an Island instance with the specified grid size and animal counts."""
    """Precondition: n is a positive integer, prey_count, predator_count, and human_count are non-negative integers."""
    """Raises: ValueError if the total number of animals exceeds the number of available cells in the grid."""
    """Parameters: n - An integer representing the size of the grid (n x n), prey_count - An integer representing the initial number of prey, predator_count - An integer representing the initial number of predators, human_count - An integer representing the initial number of humans."""
    """Usage: Create an Island instance with the desired grid size and animal counts, and use its methods to simulate the interactions between animals on the island."""
    def __init__(self, n: int, prey_count: int = 0, predator_count: int = 0, human_count: int = 0) -> None:
        """Initialize an Island instance with a grid of size n x n and populate it with the specified number of prey, predators, and humans."""
        self.grid_size: int = n
        self.grid: list[list[Cell]] = [[0] * n for _ in range(n)]
        self.init_animals(prey_count, predator_count, human_count)

    def init_animals(self, prey_count: int, predator_count: int, human_count: int) -> None:
        """Populate the island with the specified number of prey, predators, and humans."""
        empty_cells = sum(
            1 for x in range(self.grid_size)
            for y in range(self.grid_size)
            if not self.grid[x][y]
        )
        if prey_count + predator_count + human_count > empty_cells:
            raise ValueError("Too many animals for the grid size.")
        for animal_class, count in ((Prey, prey_count),
                                    (Predator, predator_count),
                                    (Human, human_count)):
            placed = 0
            while placed < count:
                x = random.randint(0, self.grid_size - 1)
                y =random.randint(0, self.grid_size - 1)
                if not self.animal(x, y):
                    self.register(animal_class(island=self, x=x, y=y))
                    placed += 1

    def clear_all_moved_flags(self) -> None:
        """Clear the moved flags for all animals on the island."""
        for animal in self.all_animals():
            animal.clear_moved_flags()

    def size(self) -> int:
        """Return the size of the island grid."""
        return self.grid_size

    def register(self, animal: Animal) -> None:
        """Register an animal on the island at its current position."""
        self.grid[animal.x][animal.y] = animal

    def remove(self, animal: Animal) -> None:
        """Remove an animal from the island."""
        self.grid[animal.x][animal.y] = 0

    def animal(self, x: int, y: int) -> Union[Cell, int]:
        """Return the animal at the specified position on the island, or -1 if out of bounds."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        return -1

    def all_animals(self) -> list[Animal]:
        """Return a list of all animals currently on the island."""
        return [self.grid[x][y] for x in range (self.grid_size) 
                for y in range(self.grid_size) if self.grid[x][y] != 0]

    def __str__(self) -> str: 
        """Return a string representation of the island grid, with animals represented by their names and empty cells by dots."""
        s = ""
        for j in range(self.grid_size - 1, -1, -1):
            for i in range(self.grid_size):
                cell = self.grid[i][j]
                s += (str(cell) if cell else ".") + " "
            s += "\n"
        return s

    def _count(self, animal_class: type) -> int:
        """Return the count of animals of a specific class on the island."""
        return sum(1 for a in self.all_animals()
                   if isinstance(a, animal_class))

    def count_prey(self) -> int:
        """Return the count of prey on the island."""
        return self._count(Prey)

    def count_predators(self) -> int:
        """Return the count of predators on the island."""
        return self._count(Predator)

    def count_humans(self) -> int:
        """Return the count of humans on the island."""
        return self._count(Human)

class Animal(object):
    """A class representing an animal on the island."""
    """Postcondition: Initializes an Animal instance with the specified island, position, and name."""
    """Precondition: island is an instance of Island, x and y are integers representing valid positions on the island, and s is a string representing the animal's name."""
    """Raises: TypeError if island is not an Island instance, x or y are not integers, or s is not a string. ValueError if x or y are out of bounds for the island grid."""
    """Parameters: island - An instance of Island representing the island the animal is on, x - An integer representing the x-coordinate of the animal's position, y - An integer representing the y-coordinate of the animal's position, s - A string representing the animal's name."""
    """Usage: Create an Animal instance with the desired island, position, and name, and use its methods to simulate the animal's behavior on the island."""
    def __init__(self, island: Island, x: int, y: int, s: str = "A") -> None:
        """Initialize an Animal instance with the specified island, position, and name."""
        self.island: Island = island
        self.x: int = x
        self.y: int = y
        self.moved: bool = False
        self.breed_clock: int = 0
        self.alive: bool = True
        self.name = s

    def position(self) -> Location:
        """Return the current position of the animal as a tuple (x, y)."""
        return (self.x, self.y)

    def __str__(self) -> str:
        """Return a string representation of the animal, which is its name."""
        return self.name

    def check_grid(self, type_looking_for: type = int) -> Union[Location, int]:
        """Check the surrounding grid cells for a specific type of animal or empty cell."""
        offset = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in offset:
            x = self.x + dx
            y = self.y + dy
            size = self.island.size()
            if not (0 <= x < size and 0 <= y < size):
                continue
            if type(self.island.animal(x, y)) == type_looking_for:
                return (x, y)
        return 0

    def move(self) -> None:
        """Move the animal to an adjacent empty cell if possible."""
        if self.breed_clock <= 0:
            location = self.check_grid(int)
            if location:
                self.breed_clock = self.breed_time
                the_class = self.__class__
                new_animal = the_class(self.island, x=location[0], 
                                       y=location[1])
                self.island.register(new_animal)

    def breed(self) -> None:
        """Breed a new animal in an adjacent empty cell if the breed clock has reached zero."""
        if self.breed_clock <= 0:
            location = self.check_grid(int)
            if location:
                self.breed_clock = self.breed_time
                the_class = self.__class__
                new_animal = the_class(self.island, x=location[0], 
                                       y=location[1])
                self.island.register(new_animal)
                self.breed_clock = self.breed_time

    def eat(self) -> None:
        """Eat an adjacent animal of a specific type if possible, resetting the starve clock."""
        pass

    def clock_tick(self) -> None:
        self.breed_clock -= 1

    def _hunt(self, food_type: type) -> None:
        """Sets the hunt attribute to the island and to the classes"""
        if self.moved:
            return False
        location = self.check_grid(food_type)
        if not location:
            return False
        self.island.remove(self.island.animal(location[0], location[1]))
        self.island.remove(self)
        self.x, self.y = location
        self.island.register(self)
        self.moved = True
        return True

    def clear_moved_flags(self) -> None:
        self.moved = False

class Prey(Animal):
    """A prey animal and it moves and breeds every Prey.breed_time ticks."""
    def __init__(self, island: Island, x: int= 0, y: int = 0, 
                 s: str = "0") -> None:
        super().__init__(island, x, y, s)
        self.breed_clock = self.breed_time

class Predator(Animal):
    """A predator and its eats the neighboring Prey, moves, breeds, and starves."""
    starve_time: int

    def __init__(self, island: Island, x: int = 0, y: int = 0, s: str = "X") -> None:
        """Creates the predator
        Precondition: Predator.breed_time and Predator.starve_time
        Postcondition: starve_clock == starve_time and breed_clock == breed_time"""
        super().__init__(island, x, y, s)
        self.starve_clock = self.starve_time
        self.breed_clock = self.breed_time

    def eat(self) -> None:
        if self._hunt(Prey):
            self.starve_clock = self.starve_time

class Human(Animal):
    """The exact same as the Prey and Predator but adds both prey and predator to thge starve clock depending on when the prey is eaten"""
    """Postcondition: has three clocks starve, hunt, and breeding"""
    starve_time: int
    hunt_time: int

    def __init__(self, island: Island, x: int = 0, y: int = 0, 
                 s: str = "H") -> None:
        super().__init__(island, x, y, s)
        self.breed_clock = self.breed_time
        self.starve_clock: int = self.starve_time
        self.hunt_clock: int = self.hunt_time

    def clock_tick(self) -> None:
        super().clock_tick()
        self.starve_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None: 
        if self.hunt_clock > 0: 
            self.hunt_clock -= 1
            return
        self.hunt_clock = self.hunt_time
        if self._hunt(Predator):
            self.starve_clock = self.starve_time

def main(predator_breed_time: int = 6, predator_starve_time: int = 4, 
        initial_predators: int = 40, prey_breed_time: int = 3, 
        initial_prey: int = 200, size: int = 20, ticks: int = 1000,
        human_breed_time: int = 12, human_starve_time: int = 10, human_hunt_time: int = 5,
        initial_humans: int = 40, stable_ticks: int = 20, seed: Optional[int] = None,
        show_plot: bool = True) -> tuple[list[int], list[int], list[int]]:
        """This runs the simulation and prints the island. The parameters are"""

        if seed is not None:
            random.seed(seed)

        Predator.breed_time = predator_breed_time
        Predator.starve_time = predator_starve_time
        Prey.breed_time = prey_breed_time
        Human.breed_time = human_breed_time
        Human.starve_time = human_starve_time
        Human.hunt_time = human_hunt_time

        predator_list: list[int] = []
        prey_list: list[int] = []
        human_list: list[int] = []

        isle = Island(size, initial_prey, initial_predators, initial_humans)
        print("Initial island:")
        print(isle)

        stop_reason = f"Reached the max {ticks} ticks."
        for i in range(ticks):
            isle.clear_all_moved_flags()
            for animal in isle.all_animals():
                animal.eat()
            for animal in isle.all_animals():
                animal.move()
            for animal in isle.all_animals():
                animal.clock_tick()
            for animal in isle.all_animals():
                animal.breed()

            predator_list.append(isle.count_predators())
            prey_list.append(isle.count_prey())
            human_list.append(isle.count_humans())

            if i % stable_ticks == 0:
                print(f"Island after {i} ticks:")
                print(isle)

            if (isle.count_predators() == 0 and 
                isle.count_prey() == 0 and 
                isle.count_humans() == 0):
                stop_reason = f"All animals have died after {i} ticks."
                break

        print(stop_reason)
        print(f"Predators: {isle.count_predators()}, Prey: {isle.count_prey()}, Humans: {isle.count_humans()}")
        print("Final island:")
        print(isle)

        if show_plot:
            plt.plot(predator_list, label="Predators")
            plt.plot(prey_list, label="Prey")
            plt.plot(human_list, label="Humans")
            plt.xlabel("Ticks")
            plt.ylabel("Population")
            plt.title("Population Dynamics on the Island")
            plt.legend()
            plt.show()
        return prey_list, predator_list, human_list

if __name__ == "__main__":
    main()


