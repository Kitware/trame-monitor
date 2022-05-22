from .resource import CPUMonitor, MemoryMonitor, ProcessMonitor

COUNT = 0


def initialize(server):
    cpu = CPUMonitor(server)
    mem = MemoryMonitor(server)

    def start(**kwargs):
        global COUNT
        COUNT += 1
        if COUNT == 1:
            cpu.start()
            mem.start()

    def stop(**kwargs):
        global COUNT
        COUNT -= 1
        if COUNT == 0:
            cpu.stop()
            mem.stop()

    @server.state.change("refresh_rate")
    def update_refresh_rate(refresh_rate, **kwargs):
        ctrl.resource_update_refresh_rate(refresh_rate)

    ctrl = server.controller
    ctrl.on_client_connected.add(start)
    ctrl.on_client_exited.add(stop)

    ctrl.resource_update_refresh_rate.add(cpu.update_refresh_rate)
    ctrl.resource_update_refresh_rate.add(mem.update_refresh_rate)