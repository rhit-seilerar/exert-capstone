from collections.abc import Callable
from pandare import Panda
from exert.utilities.types import aarch64_types,arm_types,i386_types,x86_64_types

type CPUState = (aarch64_types.CPUState |
                 arm_types.CPUState |
                 i386_types.CPUState |
                 x86_64_types.CPUState)

ExertCallable = Callable[[Panda, CPUState], None]