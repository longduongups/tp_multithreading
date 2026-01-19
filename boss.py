from task import Task
from queue_client import QueueClient


class Boss(QueueClient):
    def submit_tasks(self, n: int, size: int | None = None):
        for i in range(n):
            self.task_queue.put(Task(identifier=i, size=size))

    def collect_results(self, n: int):
        results = []
        for _ in range(n):
            results.append(self.result_queue.get())
        return results

    def stop_minions(self, n_minions: int):
        for _ in range(n_minions):
            self.task_queue.put("STOP")


def main():
    boss = Boss()

    n_tasks = 5
    n_minions = 1  # nombre de minions lancés

    boss.submit_tasks(n=n_tasks, size=200)
    results = boss.collect_results(n=n_tasks)

    for t in results:
        print(f"Task {t.identifier}: size={t.size}, time={t.time:.4f}s")

    # arrêt propre
    boss.stop_minions(n_minions)


if __name__ == "__main__":
    main()
