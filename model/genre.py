from dataclasses import dataclass

@dataclass
class Genre:
    GenreId: int
    Name: str

    def __hash__(self):
        return hash(self.GenreID)

    def __eq__(self, other):
        return self.GenreID == other.GenreID

    def __str__(self):
        return self.Name