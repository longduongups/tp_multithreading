from multiprocessing.managers import BaseManager
from queue import Queue

_TASK_QUEUE: Queue = Queue()
_RESULT_QUEUE: Queue = Queue()


def get_task_queue() -> Queue:
    return _TASK_QUEUE


def get_result_queue() -> Queue:
    return _RESULT_QUEUE


class QueueManager(BaseManager):
    pass


# Enregistre des "factories" accessibles à distance
QueueManager.register("task_queue", callable=get_task_queue)
QueueManager.register("result_queue", callable=get_result_queue)


def main(host: str = "127.0.0.1", port: int = 50000, authkey: bytes = b"secret"):
    manager = QueueManager(address=(host, port), authkey=authkey)
    server = manager.get_server()
    print(f"QueueManager server listening on {host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
