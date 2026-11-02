# Michael Koppelmann Z23649817

from __future__ import annotations 
from numbers import Real
from typing import Union 

Number = Union[int, float]
FeeSchedule = dict[str, Number]

class ParkingPermit:
    """A class representing a parking permit."""
    """Postcondition: Initializes a ParkingPermit instance with the specified owner, months, and fee_schedule."""
    """Precondition: owner is a non-empty string, months is a positive integer, and fee_schedule is a dictionary with required fees."""
    """Raises: TypeError if owner is not a string, months is not an int, or fee_schedule is not a dict. ValueError if owner is empty, months is less than 1, or fee_schedule is missing required fees."""
    """Parameters: owner - A string representing the owner of the permit, months - An integer representing the number of months for the permit, fee_schedule - A dictionary containing the fee schedule for the permit."""
    REQUIRED_FEES: tuple[str, ...] = ("monthly",)

    def __init__(self, owner: str, months: int, fee_schedule: FeeSchedule) -> None:
        """Initialize a ParkingPermit instance."""
        if not isinstance(owner, str):
            raise TypeError("owner must be a str")
        if not owner:
            raise ValueError("owner must not be empty")
        if isinstance(months, bool) or not isinstance(months, int):
            raise TypeError("months must be an int")
        if months < 1:
            raise ValueError("months must be at least 1")
        if not isinstance(fee_schedule, dict):
            raise TypeError("fee_schedule must be a dict")
        for key in self.REQUIRED_FEES:
            if key not in fee_schedule:
                raise ValueError(f"fee_schedule is missing the fee {key!r}")
            fee = fee_schedule[key]
            if isinstance(fee, bool) or not isinstance(fee, Real):
                raise TypeError(f"fee {key!r} must be a number")
            if fee < 0:
                raise ValueError(f"fee {key!r} must not be negative")

        self.owner: str = owner
        self.months: int = months
        self.fee_schedule: FeeSchedule = dict(fee_schedule)

    def cost(self) -> float:
        """Calculate the total cost of the parking permit."""
        return self.months * self.fee_schedule["monthly"]

    def _details(self) -> str:
        """Return a string with additional details about the permit."""
        return ""

    def __str__(self) -> str:
        """Return a string representation of the parking permit."""
        return (f"{type(self).__name__} for {self.owner}: {self.months} months, cost=${self.cost():.2f}")

    def __repr__(self) -> str:
        """Return a detailed string representation of the parking permit."""
        return f"ParkingPermit({self.owner!r}, {self.months}, {self.fee_schedule!r})"

class StudentPermit(ParkingPermit):
    """A class representing a student parking permit."""
    """Postcondition: Initializes a StudentPermit instance with the specified owner, months, fee_schedule, and vehicles."""
    """Precondition: owner is a non-empty string, months is a positive integer, fee_schedule is a dictionary with required fees, and vehicles is a positive integer."""
    """Raises: TypeError if owner is not a string, months is not an int, fee_schedule is not a dict, or vehicles is not an int. ValueError if owner is empty, months is less than 1, fee_schedule is missing required fees, or vehicles is less than 1."""
    """Parameters: owner - A string representing the owner of the permit, months - An integer representing the number of months for the permit, fee_schedule - A dictionary containing the fee schedule for the permit, vehicles - An integer representing the number of vehicles allowed on the permit."""
    REQUIRED_FEES: tuple[str, ...] = ("monthly", "student_vehicle_fee", "student_base")

    def __init__(self, owner: str, months: int, fee_schedule: FeeSchedule, vehicles: int = 1) -> None:
        """Initialize a StudentPermit instance."""
        """Postcondition: Initializes a StudentPermit instance with the specified owner, months, fee_schedule, and vehicles."""
        """Precondition: owner is a non-empty string, months is a positive integer, fee_schedule is a dictionary with required fees, and vehicles is a positive integer."""
        """Raises: TypeError if owner is not a string, months is not an int, fee_schedule is not a dict, or vehicles is not an int. ValueError if owner is empty, months is less than 1, fee_schedule is missing required fees, or vehicles is less than 1."""
        super().__init__(owner, months, fee_schedule)
        if isinstance(vehicles, bool) or not isinstance(vehicles, int):
            raise TypeError("vehicles must be an int")
        if vehicles < 1:
            raise ValueError("vehicles must be at least 1")
        
        self.vehicles: int = vehicles
        self.student_vehicle_fee: float = self.fee_schedule["student_vehicle_fee"]
        self.student_base_fee: float = self.fee_schedule["student_base"]

    def cost(self) -> float:
        """Calculate the total cost of the student parking permit."""
        return self.student_base_fee + (
            (self.vehicles - 1) * self.student_vehicle_fee
        )

    def _details(self) -> str:
        """Return a string with additional details about the student permit."""
        return f"Student vehicle fee: ${self.student_vehicle_fee:.2f}"

    def __repr__(self) -> str:
        """Return a detailed string representation of the student parking permit."""
        return f"StudentPermit({self.owner!r}, {self.months}, vehicles={self.vehicles})"

class FacultyPermit(ParkingPermit):
    """A class representing a faculty parking permit."""
    """Postcondition: Initializes a FacultyPermit instance with the specified owner, months, fee_schedule, and garage_access."""
    """Precondition: owner is a non-empty string, months is a positive integer, fee_schedule is a dictionary with required fees, and garage_access is a boolean."""
    """Raises: TypeError if owner is not a string, months is not an int, fee_schedule is not a dict, or garage_access is not a bool. ValueError if owner is empty, months is less than 1, or fee_schedule is missing required fees."""
    """Parameters: owner - A string representing the owner of the permit, months - An integer representing the number of months for the permit, fee_schedule - A dictionary containing the fee schedule for the permit, garage_access - A boolean indicating whether the permit includes garage access."""
    REQUIRED_FEES: tuple[str, ...] = ("monthly", "garage_monthly", "faculty_monthly")

    def __init__(self, owner: str, months: int, fee_schedule: FeeSchedule, garage_access: bool = False) -> None:
        """Initialize a FacultyPermit instance."""
        super().__init__(owner, months, fee_schedule)
        if not isinstance(garage_access, bool):
            raise TypeError("garage_access must be a bool")
        self.garage_access: bool = garage_access

    def cost(self) -> float:
        """Calculate the total cost of the faculty parking permit."""
        total = self.months * self.fee_schedule["faculty_monthly"]
        
        if self.garage_access:
            total += self.months * self.fee_schedule["garage_monthly"]
        
        return total

    def _details(self) -> str:
        """Return a string with additional details about the faculty permit."""
        return f"Garage access: {'Yes' if self.garage_access else 'No'}"

    def __repr__(self) -> str:
        """Return a detailed string representation of the faculty parking permit."""
        return f"FacultyPermit({self.owner!r}, {self.months}, garage_access={self.garage_access})"

def summarize_list(permits: list[ParkingPermit]) -> float:
    total_revenue = 0.0
    total_vehicles = 0

    for permit in permits:
        print(str(permit))
        print(repr(permit))

        if isinstance(permit, StudentPermit):
            total_vehicles += permit.vehicles
    
        total_revenue += permit.cost()

    print(f"Total vehicles for student permits: {total_vehicles}")
    
    return total_revenue

def main() -> None:
    fee_schedule = {
        "monthly": 100.0,
        "student_base": 150.00,
        "student_vehicle_fee": 10.0,
        "garage_monthly": 15.0,
        "faculty_monthly": 40.0,
    }

    permits = [
        ParkingPermit("Alice", 3, fee_schedule),
        StudentPermit("Bob", 6, fee_schedule, vehicles=3),
        FacultyPermit("Charlie", 12, fee_schedule, garage_access=True),
    ]

    total = summarize_list(permits)
    print(f"Total of parking revenue: ${total:.2f}")

if __name__ == "__main__":
    main()

