import unittest

from task import Task


class TestTaskJson(unittest.TestCase):
    def test_roundtrip_json(self):
        a = Task(identifier=123, size=10)
        a.work()  # pour remplir x et time

        txt = a.to_json()
        b = Task.from_json(txt)

        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
