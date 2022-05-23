import time
import asyncio
import importlib
import multiprocessing
from functools import partial
from concurrent.futures import ProcessPoolExecutor

from trame.app import get_server, asynchronous


def run_trame_app(process_key, module_path, queue, t0):
    with asynchronous.StateQueue(queue) as state:
        server = get_server(process_key)

        def on_ready(**_):
            state[process_key] = {
                "status": "ready",
                "port": server.port,
                "cmd": module_path,
                "start_time": time.time() - t0,
            }

        def free_process(**_):
            asynchronous.create_task(server.stop())

        server.controller.on_server_ready.add(on_ready)
        server.controller.on_client_exited.add(free_process)

        # Fill server with app
        m = importlib.import_module(module_path)
        m.main(
            server,
            port=0,
            open_browser=False,
        )

        state[process_key] = {
            "status": "exited",
            "port": server.port,
            "cmd": module_path,
            "start_time": time.time() - t0,
        }


class ProcessLauncherManager:
    def __init__(self, server=None, nb_proc_max=10):
        self._manager = multiprocessing.Manager()
        self._pool_context = multiprocessing.get_context("spawn")
        self._pool = ProcessPoolExecutor(nb_proc_max, mp_context=self._pool_context)
        self._next_pid = 1
        self._server = server

        server.state.processes = []
        server.controller.launcher_start = self.start

    def start(self, module_path):
        asynchronous.create_task(self._start(module_path))

    async def _start(self, module_path):
        with self._server.state as state:
            process_key = f"process_{self._next_pid}"
            self._next_pid += 1
            state[process_key] = {
                "status": "starting",
                "cmd": module_path,
            }
            state.processes += [process_key]
            queue = self._manager.Queue()
            loop = asyncio.get_event_loop()
            loop.run_in_executor(
                self._pool,
                partial(run_trame_app, process_key, module_path, queue, time.time()),
            )

            asynchronous.create_state_queue_monitor_task(self._server, queue, delay=0.5)
