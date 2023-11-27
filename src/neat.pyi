"""NEAT Library Implemented in C and CUDA"""


class GenerationManager:
    """Manages all functionality for a NEAT generation."""

    POPULATION_SIZE: int
    """The size of a generation."""
    generation_number: int
    """The current generation's number."""

    def get_current_best(self) -> Creature:
        """Returns the best Creature in the current generation."""

    def get_current_generation(self) -> list[Creature]:
        """Returns all Creatures in this generation."""

    #def get_generation_number(self) -> int:
    #    """Returns the current generation's number."""

    def save_generation(self, ranking: int, file: str) -> bool:
        """
        Saves the current sorted generation into the specified file.

        Returns True if process succeeded, False otherwise.
        """

    def load_generation(self, file: str) -> bool:
        """
        Loads the generation from the specified file.
        Overwrites the currently loaded generation.

        Returns True if process succeeded, False otherwise.
        """

    def evolve(self, ranking: int) -> bool:
        """
        Evolves one generation.
        Receives a pointer to the rankings.

        Returns True if process succeeded, False otherwise.
        """


class Creature:
    """An individual Creature which can play Chinese Checkers."""

    node_count: int
    connection_count: int

    def calculate(self, board: int, output_buf: int) -> None:
        """
        Takes a pointer to a board and an output buffer, and
        fills the buffer with calculated confidences for each move.

        The board should be of size 81.
        The output buffer should be of size x.
        """

    def total_gene_count(self) -> int:
        """a"""







def maxmul(a: int, b: int, c: int, size: int) -> None:
    """Temporary thing to test CUDA"""



