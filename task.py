import time
import numpy as np
import json


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
        payload = {
            "identifier": self.identifier,
            "size": self.size,
            "a": self.a.tolist(),
            "b": self.b.tolist(),
            "x": self.x.tolist(),
            "time": float(self.time),
        }
        return json.dumps(payload)

    @staticmethod
    def from_json(text: str) -> "Task":
        data = json.loads(text)

        size = int(data["size"])
        t = Task(identifier=int(data["identifier"]), size=size)

        # A
        a_raw = data.get("a", None)
        if a_raw is None or a_raw == []:
            t.a = np.random.rand(size, size)
        else:
            if isinstance(a_raw[0], list):
                t.a = np.array(a_raw, dtype=float)
            else:
                t.a = np.array(a_raw, dtype=float).reshape((size, size))

        # b
        b_raw = data.get("b", None)
        if b_raw is None or b_raw == []:
            t.b = np.random.rand(size)
        else:
            t.b = np.array(b_raw, dtype=float).reshape((size,))

        #  x / time
        x_raw = data.get("x", None)
        if x_raw is None or x_raw == []:
            t.x = np.zeros(size)
        else:
            t.x = np.array(x_raw, dtype=float).reshape((size,))

        t.time = float(data.get("time", 0.0))
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
        # x peut être None
        if self.x is None and other.x is None:
            pass
        elif (self.x is None) != (other.x is None):
            return False
        else:
            if not np.allclose(self.x, other.x):
                return False

        # time : tolérance aussi (float)
        return abs(float(self.time) - float(other.time)) < 1e-12
