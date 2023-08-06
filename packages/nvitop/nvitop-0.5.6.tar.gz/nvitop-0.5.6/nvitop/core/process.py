# This file is part of nvitop, the interactive NVIDIA-GPU process viewer.
# License: GNU GPL version 3.

# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
# pylint: disable=invalid-name

import contextlib
import datetime
import functools
import os
import threading
from abc import ABCMeta
from types import FunctionType
from typing import List, Iterable, Callable, Union, Optional, Any, TYPE_CHECKING

from nvitop.core import host
from nvitop.core.libnvml import nvml
from nvitop.core.utils import (NA, NaType, Snapshot,
                               bytes2human, timedelta2human,
                               utilization2string, memoize_when_activated)


if TYPE_CHECKING:
    from nvitop.core.device import Device


__all__ = ['HostProcess', 'GpuProcess', 'command_join']


if host.POSIX:
    def add_quotes(s: str) -> str:
        if s == '':
            return '""'
        if '$' not in s and '\\' not in s and '\n' not in s:
            if ' ' not in s:
                return s
            if '"' not in s:
                return '"{}"'.format(s)
        if "'" not in s and '\n' not in s:
            return "'{}'".format(s)
        return '"{}"'.format(s.replace('\\', r'\\').replace('"', r'\"')
                              .replace('$', r'\$').replace('\n', r'\n'))
elif host.WINDOWS:
    def add_quotes(s: str) -> str:
        if s == '':
            return '""'
        if '%' not in s and '^' not in s and '\n' not in s:
            if ' ' not in s:
                return s
            if '"' not in s:
                return '"{}"'.format(s)
        return '"{}"'.format(s.replace('^', '^^').replace('"', '^"')
                              .replace('%', '^%').replace('\n', r'\n'))
else:
    def add_quotes(s: str) -> str:
        return '"{}"'.format(s.replace('\n', r'\n'))


def command_join(cmdline: List[str]) -> str:
    if len(cmdline) > 1:
        cmdline = '\0'.join(cmdline).strip('\0').split('\0')
    if len(cmdline) == 1 and not (os.path.isfile(cmdline[0]) and os.path.isabs(cmdline[0])):
        return cmdline[0]
    return ' '.join(map(add_quotes, cmdline))


def auto_garbage_clean(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapped(self: 'GpuProcess', *args, **kwargs) -> Any:
        try:
            return func(self, *args, **kwargs)
        except host.PsutilError:
            try:
                with GpuProcess.INSTANCE_LOCK:
                    del GpuProcess.INSTANCES[(self.pid, self.device)]
            except KeyError:
                pass
            try:
                with HostProcess.INSTANCE_LOCK:
                    del HostProcess.INSTANCES[self.pid]
            except KeyError:
                pass

            raise

    return wrapped


class HostProcess(host.Process, metaclass=ABCMeta):
    INSTANCE_LOCK = threading.RLock()
    INSTANCES = {}

    def __new__(cls, pid: Optional[int] = None) -> 'HostProcess':
        if pid is None:
            pid = os.getpid()

        with cls.INSTANCE_LOCK:
            try:
                instance = cls.INSTANCES[pid]
                if instance.is_running():
                    return instance
            except KeyError:
                pass

            instance = super().__new__(cls)

            instance._super_gone = False
            host.Process._init(instance, pid, True)
            try:
                host.Process.cpu_percent(instance)
            except host.PsutilError:
                pass

            cls.INSTANCES[pid] = instance

            return instance

    def __init__(self, pid: Optional[int] = None) -> None:  # pylint: disable=unused-argument,super-init-not-called
        pass

    @property
    def _gone(self) -> bool:
        return self._super_gone

    @_gone.setter
    def _gone(self, value: bool) -> None:
        if value:
            with self.INSTANCE_LOCK:
                try:
                    del self.INSTANCES[self.pid]
                except KeyError:
                    pass
        self._super_gone = value

    def __str__(self) -> str:
        return super().__str__().replace(self.__class__.__module__ + '.', '', 1)

    __repr__ = __str__

    if host.WINDOWS:
        def username(self) -> str:
            return super().username().split('\\')[-1]

    cmdline = memoize_when_activated(host.Process.cmdline)

    def command(self) -> str:
        return command_join(self.cmdline())

    @memoize_when_activated
    def running_time(self) -> datetime.timedelta:
        return datetime.datetime.now() - datetime.datetime.fromtimestamp(self.create_time())

    def running_time_human(self) -> str:
        return timedelta2human(self.running_time())

    def parent(self) -> Union['HostProcess', None]:
        parent = super().parent()
        if parent is not None:
            return HostProcess(parent.pid)
        return None

    def children(self, recursive: bool = False) -> List['HostProcess']:
        return [HostProcess(child.pid) for child in super().children(recursive)]

    @contextlib.contextmanager
    def oneshot(self):
        with self._lock:
            if hasattr(self, '_cache'):
                yield
            else:
                with super().oneshot():
                    # pylint: disable=no-member
                    try:
                        self.cmdline.cache_activate(self)
                        self.running_time.cache_activate(self)
                        yield
                    finally:
                        self.cmdline.cache_deactivate(self)
                        self.running_time.cache_deactivate(self)

    def as_snapshot(self, attrs: Optional[Iterable[str]] = None, ad_value: Optional[Any] = None) -> Snapshot:
        with self.oneshot():
            attributes = self.as_dict(attrs=attrs, ad_value=ad_value)

            if attrs is None:
                for attr in ('command', 'running_time', 'running_time_human'):
                    try:
                        attributes[attr] = getattr(self, attr)()
                    except (host.AccessDenied, host.ZombieProcess):
                        attributes[attr] = ad_value

        return Snapshot(real=self, **attributes)


class GpuProcess:  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    INSTANCE_LOCK = threading.RLock()
    INSTANCES = {}

    def __new__(cls, pid: int, device: 'Device',
                gpu_memory: Optional[Union[int, NaType]] = None,  # pylint: disable=unused-argument
                type: Optional[Union[str, NaType]] = None) -> 'GpuProcess':  # pylint: disable=unused-argument,redefined-builtin
        if pid is None:
            pid = os.getpid()

        with cls.INSTANCE_LOCK:
            try:
                instance = cls.INSTANCES[(pid, device)]
                if instance.is_running():
                    return instance
            except KeyError:
                pass

            instance = super().__new__(cls)

            instance._pid = pid
            instance._host = HostProcess(pid)
            instance._ident = (*instance._host._ident, device.index)
            instance._device = device

            instance._hash = None
            instance._username = None

            cls.INSTANCES[(pid, device)] = instance

            return instance

    def __init__(self, pid: int, device: 'Device',  # pylint: disable=unused-argument
                 gpu_memory: Optional[Union[int, NaType]] = None,
                 type: Optional[Union[str, NaType]] = None) -> None:  # pylint: disable=redefined-builtin
        if gpu_memory is None and not hasattr(self, '_gpu_memory'):
            gpu_memory = NA
        if gpu_memory is not None:
            self.set_gpu_memory(gpu_memory)
        if type is None and not hasattr(self, '_type'):
            type = NA
        if type is not None:
            self.type = type
        for util in ('sm', 'memory', 'encoder', 'decoder'):
            if not hasattr(self, '_gpu_{}_utilization'.format(util)):
                setattr(self, '_gpu_{}_utilization'.format(util), 0)

    def __str__(self) -> str:
        return '{}(pid={}, gpu_memory={}, type={}, device={}, host={})'.format(
            self.__class__.__name__,
            self.pid, self.gpu_memory_human(), self.type,
            self.device, self.host
        )

    __repr__ = __str__

    def __eq__(self, other: Union[host.Process, 'GpuProcess']) -> bool:
        if not isinstance(other, (GpuProcess, host.Process)):
            return NotImplemented
        return self._ident == other._ident

    def __ne__(self, other: Union[host.Process, 'GpuProcess']) -> bool:
        return not self == other

    def __hash__(self) -> int:
        if self._hash is None:  # pylint: disable=access-member-before-definition
            self._hash = hash(self._ident)  # pylint: disable=attribute-defined-outside-init
        return self._hash

    def __getattr__(self, name: str) -> Union[Any, Callable[..., Any]]:
        try:
            return super().__getattr__(name)
        except AttributeError:
            attribute = getattr(self.host, name)
            if isinstance(attribute, FunctionType):
                attribute = auto_garbage_clean(attribute)

            setattr(self, name, attribute)
            return attribute

    @property
    def pid(self) -> int:
        return self._pid

    @property
    def host(self) -> HostProcess:
        return self._host

    @property
    def device(self) -> 'Device':
        return self._device

    def gpu_memory(self) -> Union[int, NaType]:  # in bytes
        return self._gpu_memory

    def gpu_memory_human(self) -> Union[str, NaType]:  # in human readable
        return self._gpu_memory_human

    def gpu_memory_percent(self) -> Union[float, NaType]:  # in percentage
        return self._gpu_memory_percent

    def gpu_sm_utilization(self) -> int:  # in percentage
        return self._gpu_sm_utilization

    def gpu_memory_utilization(self) -> int:  # in percentage
        return self._gpu_memory_utilization

    def gpu_encoder_utilization(self) -> int:  # in percentage
        return self._gpu_encoder_utilization

    def gpu_decoder_utilization(self) -> int:  # in percentage
        return self._gpu_decoder_utilization

    def set_gpu_memory(self, value: Union[int, NaType]) -> None:
        self._gpu_memory = memory_used = value  # pylint: disable=attribute-defined-outside-init
        self._gpu_memory_human = bytes2human(self.gpu_memory())  # pylint: disable=attribute-defined-outside-init
        memory_total = self.device.memory_total()
        gpu_memory_percent = NA
        if nvml.nvmlCheckReturn(memory_used, int) and nvml.nvmlCheckReturn(memory_total, int):
            gpu_memory_percent = round(100.0 * memory_used / memory_total, 1)
        self._gpu_memory_percent = gpu_memory_percent  # pylint: disable=attribute-defined-outside-init

    def set_gpu_utilization(self, gpu_sm_utilization: int = 0,
                            gpu_memory_utilization: int = 0,
                            gpu_encoder_utilization: int = 0,
                            gpu_decoder_utilization: int = 0) -> None:
        self._gpu_sm_utilization = gpu_sm_utilization  # pylint: disable=attribute-defined-outside-init
        self._gpu_memory_utilization = gpu_memory_utilization  # pylint: disable=attribute-defined-outside-init
        self._gpu_encoder_utilization = gpu_encoder_utilization  # pylint: disable=attribute-defined-outside-init
        self._gpu_decoder_utilization = gpu_decoder_utilization  # pylint: disable=attribute-defined-outside-init

    def update_gpu_status(self) -> Union[int, NaType]:
        self.device.processes.cache_clear()
        self.device.processes()
        return self.gpu_memory()

    @property
    def type(self) -> Union[str, NaType]:
        return self._type

    @type.setter
    def type(self, value: Union[str, NaType]) -> None:
        if 'C' in value and 'G' in value:
            self._type = 'C+G'
        elif 'C' in value:
            self._type = 'C'
        elif 'G' in value:
            self._type = 'G'
        else:
            self._type = NA

    @auto_garbage_clean
    def is_running(self) -> bool:
        return self.host.is_running()

    @auto_garbage_clean
    def status(self) -> str:
        return self.host.status()

    @auto_garbage_clean
    def create_time(self) -> float:
        return self.host.create_time()

    @auto_garbage_clean
    def running_time(self) -> datetime.timedelta:
        return self.host.running_time()

    def running_time_human(self) -> str:
        return timedelta2human(self.running_time())

    @auto_garbage_clean
    def username(self) -> str:
        if self._username is None:  # pylint: disable=access-member-before-definition
            self._username = self.host.username()  # pylint: disable=attribute-defined-outside-init
        return self._username

    @auto_garbage_clean
    def name(self) -> str:
        return self.host.name()

    @auto_garbage_clean
    def cpu_percent(self) -> float:
        return self.host.cpu_percent()

    @auto_garbage_clean
    def memory_percent(self) -> float:
        return self.host.memory_percent()

    @auto_garbage_clean
    def cmdline(self) -> List[str]:
        return self.host.cmdline()

    def command(self) -> str:
        return command_join(self.cmdline())

    @auto_garbage_clean
    def as_snapshot(self) -> Snapshot:
        with self.host.oneshot():
            host_snapshot = Snapshot(
                real=self.host,
                is_running=self.is_running(),
                status=self.status(),
                username=self.username(),
                name=self.name(),
                cmdline=self.cmdline(),
                command=self.command(),
                cpu_percent=self.cpu_percent(),
                memory_percent=self.memory_percent(),
                running_time=self.running_time(),
                running_time_human=self.running_time_human()
            )

        return Snapshot(
            real=self,
            pid=self.pid,
            device=self.device,
            gpu_memory=self.gpu_memory(),
            gpu_memory_human=self.gpu_memory_human(),
            gpu_memory_percent=self.gpu_memory_percent(),
            gpu_sm_utilization=self.gpu_sm_utilization(),
            gpu_memory_utilization=self.gpu_memory_utilization(),
            gpu_encoder_utilization=self.gpu_encoder_utilization(),
            gpu_decoder_utilization=self.gpu_decoder_utilization(),
            type=self.type,
            username=host_snapshot.username,
            name=host_snapshot.name,
            cmdline=host_snapshot.cmdline,
            command=host_snapshot.command,
            cpu_percent=host_snapshot.cpu_percent,
            memory_percent=host_snapshot.memory_percent,
            is_running=host_snapshot.is_running,
            running_time=host_snapshot.running_time,
            running_time_human=host_snapshot.running_time_human
        )

    def gpu_memory_percent_string(self) -> str:  # in percentage
        return utilization2string(self.gpu_memory_percent())

    def gpu_sm_utilization_string(self) -> str:  # in percentage
        return utilization2string(self.gpu_sm_utilization())

    def gpu_memory_utilization_string(self) -> str:  # in percentage
        return utilization2string(self.gpu_memory_utilization())

    def gpu_encoder_utilization_string(self) -> str:  # in percentage
        return utilization2string(self.gpu_encoder_utilization())

    def gpu_decoder_utilization_string(self) -> str:  # in percentage
        return utilization2string(self.gpu_decoder_utilization())


HostProcess.register(GpuProcess)
