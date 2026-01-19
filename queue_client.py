from multiprocessing.managers import BaseManager


class QueueClient:
    def __init__(
        self, host: str = "127.0.0.1", port: int = 50000, authkey: bytes = b"secret"
    ):
        self.host = host
        self.port = port
        self.authkey = authkey

        class _ClientManager(BaseManager):
            pass

        _ClientManager.register("task_queue")
        _ClientManager.register("result_queue")

        self.manager = _ClientManager(
            address=(self.host, self.port), authkey=self.authkey
        )
        self.manager.connect()

        self.task_queue = self.manager.task_queue()
        self.result_queue = self.manager.result_queue()
