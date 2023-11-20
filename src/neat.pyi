"""NEAT Library Implemented in C and CUDA"""

import ctypes


class NEAT:
    """Manages all functionality for NEAT."""

    def get_current_best(self) -> Creature: """Returns the best Creature in the current generation."""

    def get_current_generation(self) -> list[Creature]:
        """Returns all Creatures in this generation."""

    def get_generation_number(self) -> int:
        """Returns the current generation's number."""

    def save_generation(self, file: str) -> bool:
        """
        Saves the current generation into the specified file.

        Returns True if process succeeded, False otherwise.
        """

    def load_generation(self, file: str) -> bool:
        """
        Loads the generation from the specified file.
        Overwrites the currently loaded generation.

        Returns True if process succeeded, False otherwise.
        """

    def evolve(self) -> None:
        """Evolves one generation."""


class Creature:
    """An individual Creature which can play Chinese Checkers."""

    def calculate(self, board: ctypes.c_long, output_buf: ctypes.c_long) -> None:
        """
        Takes a pointer to a board and an output buffer, and
        fills the buffer with calculated confidences for each move.

        The board should be of size 81.
        The output buffer should be of size x.
        """

def maxmul(a: int, b: int, c: int, size: int) -> None:
    """Temporary thing to test CUDA"""





