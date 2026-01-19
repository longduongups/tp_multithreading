import time
import numpy as np


class Task:
    def __init__(self, identifier: int = 0, size: int | None = None):
        self.identifier = identifier
        self.size = int(size) if size is not None else int(np.random.randint(300, 3000))

        # Données du problème Ax = b
        self.a = np.random.rand(self.size, self.size)
        self.b = np.random.rand(self.size)

        # Résultats
        self.x = np.zeros(self.size)
        self.time = 0.0

    def work(self) -> "Task":
        start = time.perf_counter()
        self.x = np.linalg.solve(self.a, self.b)
        self.time = time.perf_counter() - start
        return self
