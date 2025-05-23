from .asyncthread import AsyncThread as AsyncThread
from .cosi import Cosi as Cosi
from .panda_expect import Expect as Expect
from .qemu_logging import QEMU_Log_Manager as QEMU_Log_Manager
from .taint import TaintQuery as TaintQuery
from .utils import GArrayIterator as GArrayIterator, debug as debug
from .arch import PandaArch
from .pypluginmanager import PyPluginManager
from cffi import FFI as FFI
from os import getenv as getenv
from os.path import abspath as abspath, dirname as dirname
from random import randint as randint
from collections.abc import Callable
from typing import Protocol, Literal
from exert.utilities.types.multi_arch import CPUState, TranslationBlock
from typing import Any
from cffi import FFI

class PPPFunction(Protocol):
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

class Panda:
    lambda_cnt: int
    ending: bool
    serial_unconsumed_data: bytes
    arch: PandaArch
    ffi: FFI
    plugin_register_count: int
    disabled_tb_chaining: bool
    def __init__(self, arch: str = 'i386', mem: str = '128M', expect_prompt: str | None = None, serial_kwargs: dict[str, Any] | None = None, os_version: str | None = None, qcow: str | bytes | None = None, os: str = 'linux', generic: str | None = None, raw_monitor: bool = False, extra_args: str | list[str] | None = None, catch_exceptions: bool = True, libpanda_path: str | bytes | None = None, biospath: str | bytes | None = None, plugin_path: str | bytes | None = None) -> None: ...
    def exit_cpu_loop(self) -> None: ...
    warned_async: bool
    def reset(self) -> None: ...
    def cont(self) -> None: ...
    def vm_stop(self, code: int = 4) -> None: ...
    def enable_tb_chaining(self) -> None: ...
    def disable_tb_chaining(self) -> None: ...
    def run(self) -> None: ...
    def end_analysis(self) -> None: ...
    def end_record(self) -> None: ...
    def end_replay(self) -> None: ...
    def unload_plugins(self) -> None: ...
    def virtual_memory_read(self, cpu: CPUState, addr: int, length: int, fmt: str = 'bytearray') -> (bytes | int | str | list[int]): ...
    def read_str(self, cpu: CPUState, ptr: int, max_length: int | None = None) -> str: ...
    def queue_blocking(self, func: Callable[[], None], queue: bool = True) -> Callable[[], None]: ...
    @property
    def pyplugins(self) -> PyPluginManager: ...
    def enable_memcb(self) -> None: ...
    def disable_memcb(self) -> None: ...
    def enable_llvm(self) -> None: ...
    def disable_llvm(self) -> None: ...
    def enable_llvm_helpers(self) -> None: ...
    def disable_llvm_helpers(self) -> None: ...
    def enable_precise_pc(self) -> None: ...
    def disable_precise_pc(self) -> None: ...
    def in_kernel(self, cpustate: CPUState) -> bool: ...
    def in_kernel_mode(self, cpustate: CPUState) -> bool: ...
    def current_sp(self, cpu: CPUState) -> int: ...
    def cleanup(self) -> None: ...
    def get_cpu(self) -> CPUState: ...
    pyperipherals_registered_cb: bool
    def taint_sym_enable(self) -> None: ...
    pos: int
    closed: bool
    mode: str
    name: str
    def stop_run(self) -> None: ...
    def run_serial_cmd(self, cmd: str, no_timeout: bool = False, timeout: int | None = None) -> str: ...
    def revert_sync(self, snapshot_name: str) -> str: ...
    def interact(self, confirm_quit: bool = True) -> None: ...
    def do_panda_finish(self) -> None: ...
    def enable_internal_callbacks(self) -> None: ...
    def enable_all_callbacks(self) -> None: ...
    def enable_callback(self, name: str) -> None: ...
    def disable_callback(self, name: str, forever: bool = False) -> None: ...
    def delete_callbacks(self) -> None: ...
    def ppp(self, plugin_name: str, attr: str, name: str | None = None, autoload: bool = True) -> Callable[[PPPFunction], PPPFunction]: ...
    def cb_guest_hypercall(self, fn: Callable[[CPUState], bool]) -> Callable[[CPUState], bool]: ...
    def cb_start_block_exec(self, fn: Callable[[CPUState, TranslationBlock], None]) -> Callable[[CPUState, TranslationBlock], None]: ...
    endianness: Literal["little", "big"]
    bits: int
    arch_name: str
    def load_plugin(self, name: str, args: dict[str, Any]) -> None: ...
    def get_processes_dict(self, cpu: CPUState) -> dict[int, dict[str, str | int]]: ...
