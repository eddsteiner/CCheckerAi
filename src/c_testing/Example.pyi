"""Test module for extending Python with C."""

def findPrimes(num1: int, num2: int) -> int:
    """Finds all primes within the range provided."""

def return_two() -> tuple[int, int]:
    """Returns two integers."""

class Custom():
    """Basic experimentation"""
    number: float 
    number1: float

class StructManager():
    """Manages a C struct"""
    x: float 
    y: float

    def add_nums(self) -> int:
        """Add x and y together."""

    def set_nums(self) -> int:
        """Set x and y."""

    def get_pointer(self) -> int:
        """Returns the pointer to the internal struct."""

    def copy_pointer(self, pointer: int) -> None:
        """Copies values from the provided pointer."""

