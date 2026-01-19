import time
import numpy as np
import json
from typing import Any


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

    def to_json(self) -> str:
        """Serialize Task to JSON (string)."""
        payload: dict[str, Any] = {
            "identifier": self.identifier,
            "size": self.size,
            "a": self.a.tolist(),
            "b": self.b.tolist(),
            "x": None if self.x is None else self.x.tolist(),
            "time": self.time,
        }
        return json.dumps(payload)

    @staticmethod
    def from_json(text: str) -> "Task":
        """Deserialize Task from JSON (string)."""
        data = json.loads(text)

        t = Task(identifier=data["identifier"], size=data["size"])

        # remplacer les valeurs aléatoires créées par __init__
        t.a = np.array(data["a"], dtype=float)
        t.b = np.array(data["b"], dtype=float)

        if data.get("x") is None:
            t.x = None
        else:
            t.x = np.array(data["x"], dtype=float)

        t.time = float(data["time"]) if data.get("time") is not None else 0.0
        return t

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return False

        # identifier/size/time
        if self.identifier != other.identifier or self.size != other.size:
            return False

        # Compare tableaux (tolérance flottante)
        if not np.allclose(self.a, other.a):
            return False
        if not np.allclose(self.b, other.b):
            return False

        # x peut être None ou un array
        if self.x is None and other.x is None:
            pass
        elif (self.x is None) != (other.x is None):
            return False
        else:
            if not np.allclose(self.x, other.x):
                return False

        # time : tolérance aussi (float)
        return abs(float(self.time) - float(other.time)) < 1e-12
