import time
import sys
import socket

from crappy.utils import Color, wait_for_keypress
from crappy.config import Config
from crappy.task import Task
from crappy.event import MasterSlaveEvent


class Slave:
    def __init__(self, config: Config):
        self.server_socket = None
        self.config = config

    def driver(self):
        self.connect_to_master()

        task = self.get_task()
        if not task or task.is_empty():
            self.handle_no_work_given()

        runtime_nano = 0
        return_code = 1

        start = time.perf_counter_ns()
        build_passed = task.execute_build()
        end = time.perf_counter_ns()

        runtime_nano = end - start
        self.print_build_status(task, build_passed, runtime_nano)
        self.send_event_to_master(
            MasterSlaveEvent.SLAVE_BUILD_SUCCESS if build_passed else MasterSlaveEvent.SLAVE_BUILD_FAILURE
        )

        if build_passed and task.has_launch():
            print(
                "{1}[BUILD][]{0} execute binary {1}`{2}`{0} with args {1}`{3}`{0}...\n"
                .format(Color["CLEAR"], Color["PURPLE"], task.tokenized_launch_cmd[0], task.tokenized_launch_cmd[1:])
            )

            start = time.perf_counter_ns()
            return_code = task.execute_launch()
            end = time.perf_counter_ns()

            runtime_nano = end - start
            self.print_launch_status(return_code, runtime_nano)

        self.disconn_from_master()
        print("Press any key to continue...", end="", flush=True)
        wait_for_keypress()

    def connect_to_master(self):
        if not self.config.sockets_enabled:
            return

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(("localhost", self.config.master_port_number))

    def send_event_to_master(self, event: MasterSlaveEvent):
        if not self.config.sockets_enabled:
            return

        self.server_socket.sendall(event.value.to_bytes(4))

    def disconn_from_master(self):
        if not self.config.sockets_enabled:
            return

        self.server_socket.close()

    def get_task(self) -> Task:
        if not self.config.task_queue or self.config.task_queue[0].is_empty():
            return None
        return self.config.task_queue[0]

    def print_build_status(self, task, build_passed, runtime_nanos):
        if not task.has_build():
            return

        print("\n\n", end="")

        if build_passed:
            print(
                "{2}[BUILD][✓]{0} completed in {1}{3}{0} with {2}no errors{0}!"
                .format(Color["CLEAR"], Color["YELLOW"], Color["GREEN"], self.get_formatted_time(runtime_nanos))
            )
        else:
            print(
                "{1}[BUILD][✗]{0} terminated at {2}{3}{0}, there are {1}some errors{0}..."
                .format(Color["CLEAR"], Color["RED"], Color["YELLOW"], self.get_formatted_time(runtime_nanos))
            )

    def print_launch_status(self, returnCode, runtimeNano):
        formattedReturnCode = self.get_formatted_return_code(returnCode)
        formattedTime = self.get_formatted_time(runtimeNano)

        print("\n\n\n", end="")
        print("Process returned {} in {}.".format(formattedReturnCode, formattedTime))

    def get_formatted_return_code(self, return_code) -> str:
        pos_return_code = return_code
        if return_code < 0:
            match Config.platform_name:
                case "Linux":
                    pos_return_code += 2 ** 8
                case "Windows":
                    pos_return_code += 2 ** 32

        result = "code {0} (0x{1:08X})".format(return_code, pos_return_code)

        color = Color["GREEN"] if return_code == 0 else Color["RED"]
        result = "{}{}{}".format(color, result, Color["CLEAR"])
        return result

    def get_formatted_time(self, nanos: int) -> str:
        micros = nanos // 1000
        millis = micros // 1000
        seconds = millis // 1000
        minutes = seconds // 60

        units = "ms"
        if minutes > 0:
            units = "min"
        elif seconds > 0:
            units = "sec"

        result = "{1}{2:02}:{3:02}.{4:03} {5}{0}".format(
            Color["CLEAR"], Color["YELLOW"], minutes, seconds % 60, millis % 1000, units
        )
        return result

    def handle_no_work_given(self):
        print(
            "{1}[BUILD][] No commands were given. There is nothing to do.{0}"
            .format(Color["CLEAR"], Color["PURPLE"])
        )
        print("Press any key to continue...", end="", flush=True)
        wait_for_keypress()
        sys.exit(0)
