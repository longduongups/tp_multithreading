from queue_client import QueueClient


class Minion(QueueClient):
    def run_forever(self):
        while True:
            task = self.task_queue.get()  # reçoit un Task
            if task == "STOP":
                break
            task.work()  # calcule
            self.result_queue.put(task)  # renvoie le Task avec x et time


def main():
    minion = Minion()
    print("Minion started, waiting for tasks...")
    minion.run_forever()


if __name__ == "__main__":
    main()
