import time
import yaml
import asyncio
import importlib
import multiprocessing
from functools import partial
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

from trame.app import get_server, asynchronous


def run_trame_app(process_key, name, module_path, queue, t0):
    if asyncio.get_event_loop().is_closed():
        asyncio.set_event_loop(asyncio.new_event_loop())

    with asynchronous.StateQueue(queue) as state:
        server = get_server(process_key)

        def on_ready(**_):
            state[process_key] = {
                "name": name,
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
            "name": name,
            "status": "exited",
            "port": server.port,
            "cmd": module_path,
            "start_time": time.time() - t0,
        }


class ProcessLauncherManager:
    def __init__(self, server=None, nb_proc_max=5, config=None):
        self._manager = multiprocessing.Manager()
        self._pool_context = multiprocessing.get_context("spawn")
        self._pool = ProcessPoolExecutor(
            max_workers=nb_proc_max, mp_context=self._pool_context
        )
        self._next_pid = 1
        self._server = server
        self._known_process_ids = set()
        self._config = {
            "applications": {
                "monitor": {
                    "module": "trame_monitor.app.main",
                },
                "cone": {
                    "module": "trame_monitor.examples.cone",
                },
                "sphere": {
                    "module": "trame_monitor.examples.sphere",
                },
            }
        }

        state, ctrl = server.state, server.controller

        state.processes = []
        state.processes_available = nb_proc_max
        state.processes_pool_size = nb_proc_max
        state.apps = []

        ctrl.launcher_start = self.start
        ctrl.launcher_clear = self.clear_exited

        state.change("processes")(self.update_listener)

        self.load_config(config)

    @property
    def state(self):
        return self._server.state

    def load_config(self, config):
        if config is not None:
            file_path = Path(config)
            if file_path.exists():
                self._config = yaml.safe_load(file_path.read_text())

        self.state.apps = list(self._config.get("applications", {}).keys())

    def update_listener(self, processes, **kwargs):
        for name in processes:
            if name not in self._known_process_ids:
                self._known_process_ids.add(name)
                self.state.change(name)(self.update_available_resources)

    def update_available_resources(self, processes, processes_pool_size, **kwargs):
        available = processes_pool_size
        for name in processes:
            status = kwargs[name].get("status")
            if status != "exited":
                available -= 1

        self.state.processes_available = available

    def clear_exited(self):
        filtered_processes = []
        for name in self.state.processes:
            status = self.state[name].get("status")
            if status != "exited":
                filtered_processes.append(name)

        self.state.processes = filtered_processes

    def start(self, app_name):
        app_config = self._config.get("applications", {}).get(app_name, {})
        module_path = app_config.get("module")
        if module_path:
            asynchronous.create_task(self._start(app_name, module_path))
        else:
            print(f"No module for app {app_name}")

    async def _start(self, name, module_path):
        with self._server.state as state:
            process_key = f"process_{self._next_pid}"
            self._next_pid += 1
            state[process_key] = {
                "name": name,
                "status": "starting",
                "cmd": module_path,
            }
            state.processes += [process_key]
            queue = self._manager.Queue()
            loop = asyncio.get_event_loop()
            loop.run_in_executor(
                self._pool,
                partial(
                    run_trame_app, process_key, name, module_path, queue, time.time()
                ),
            )

            asynchronous.create_state_queue_monitor_task(self._server, queue, delay=0.5)
