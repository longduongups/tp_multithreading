import unittest
import numpy as np
from numpy.testing import assert_allclose
from task import Task


class TestTask(unittest.TestCase):
    def test_solve(self):
        # Matrice de test
        A = np.array([[3.0, 1.0], [1.0, 2.0]])
        B = np.array([9.0, 8.0])

        task = Task(size=2)  # taille connue pour test
        task.a = A  # on injecte notre matrice A
        task.b = B  # on injecte notre vecteur B

        task.work()  # résolution

        # Vérifier que A @ x ≈ B
        assert_allclose(A @ task.x, B, rtol=1e-5, atol=1e-8)


if __name__ == "__main__":
    unittest.main()
