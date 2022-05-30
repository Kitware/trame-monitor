import psutil
import asyncio
from datetime import datetime


class AbstractMonitor:
    def __init__(self):
        self.running = False
        self._update_rate = 1.0  # seconds

    def update_refresh_rate(self, nb_sec):
        self._update_rate = nb_sec

    def start(self):
        if self.running:
            return

        self.running = True
        loop = asyncio.get_event_loop()
        task = loop.create_task(self._run())

        return task

    def stop(self):
        self.running = False

    async def _run(self):
        while self.running:
            self.update()
            await asyncio.sleep(self._update_rate)

    def update(self):
        pass


class MemoryMonitor(AbstractMonitor):
    def __init__(self, server):
        super().__init__()
        self._state = server.state
        for key in [
            "tmr_mem_total",
            "tmr_mem_available",
            "tmr_mem_percent",
            "tmr_mem_used",
            "tmr_mem_free",
            "tmr_mem_active",
            "tmr_mem_inactive",
            "tmr_mem_wired",
            "tmr_swap_percent",
            "tmr_swap_total",
            "tmr_swap_free",
            "tmr_swap_used",
        ]:
            self._state[key] = None

    def update(self):
        mem_stat = psutil.virtual_memory()
        swap_stat = psutil.swap_memory()
        with self._state:
            self._state.tmr_mem_total = mem_stat.total
            self._state.tmr_mem_available = mem_stat.available
            self._state.tmr_mem_percent = mem_stat.percent
            self._state.tmr_mem_used = mem_stat.used
            self._state.tmr_mem_free = mem_stat.free
            self._state.tmr_mem_active = mem_stat.active
            self._state.tmr_mem_inactive = mem_stat.inactive
            self._state.tmr_mem_wired = mem_stat.wired
            self._state.tmr_swap_percent = swap_stat.percent
            self._state.tmr_swap_total = swap_stat.total
            self._state.tmr_swap_free = swap_stat.free
            self._state.tmr_swap_used = swap_stat.used


class CPUMonitor(AbstractMonitor):
    def __init__(self, server):
        super().__init__()
        self._state = server.state
        for key in ["tmr_cpu_total", "tmr_cpu_per_core"]:
            self._state[key] = None

    def update(self):
        with self._state:
            self._state.tmr_cpu_total = psutil.cpu_percent()
            self._state.tmr_cpu_per_core = list(psutil.cpu_percent(percpu=True))


class ProcessMonitor(AbstractMonitor):
    def __init__(self, server):
        super().__init__()
        self._state = server.state
        self._state.tmr_process_cols = [
            "pid",
            "name",
            "create_time",
            "cores",
            "cpu_usage",
            "status",
            "nice",
            "memory_usage",
            "read_bytes",
            "write_bytes",
            "n_threads",
            "username",
        ]
        self._state.tmr_processes = []

    def update(self):
        processes = []
        for process in psutil.process_iter():
            with process.oneshot():
                pid = process.pid
                if pid == 0:
                    continue

                name = process.name()
                # try:
                #     create_time = datetime.fromtimestamp(process.create_time())
                # except OSError:
                #     # system processes, using boot time instead
                #     create_time = datetime.fromtimestamp(psutil.boot_time())

                # try:
                #     # get the number of CPU cores that can execute this process
                #     cores = len(process.cpu_affinity())
                # except psutil.AccessDenied:
                #     cores = 0

                cpu_usage = process.cpu_percent()
                status = process.status()

                # try:
                #     # get the process priority (a lower value means a more prioritized process)
                #     nice = int(process.nice())
                # except psutil.AccessDenied:
                #     nice = 0

                # try:
                #     # get the memory usage in bytes
                #     memory_usage = process.memory_full_info().uss
                # except psutil.AccessDenied:
                #     memory_usage = 0

                # total process read and written bytes
                # io_counters = process.io_counters()
                # read_bytes = io_counters.read_bytes
                # write_bytes = io_counters.write_bytes

                n_threads = process.num_threads()

                # try:
                #     username = process.username()
                # except psutil.AccessDenied:
                #     username = "N/A"

                processes.append(
                    [
                        pid,
                        name,
                        # create_time,
                        # cores,
                        cpu_usage,
                        status,
                        # nice,
                        # memory_usage,
                        # read_bytes,
                        # write_bytes,
                        n_threads,
                        # username,
                    ]
                )

        with self._state:
            # print(processes)
            self._state.tmr_processes = processes
