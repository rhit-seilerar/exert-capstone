from _typeshed import Incomplete

class PandaArch:
    panda: Incomplete
    reg_sp: Incomplete
    reg_pc: Incomplete
    reg_retaddr: Incomplete
    reg_retval: Incomplete
    call_conventions: Incomplete
    registers: Incomplete
    def get_reg(self, cpu, reg): ...
    def set_reg(self, cpu, reg, val): ...
    def get_pc(self, cpu): ...
    def set_pc(self, cpu, val): ...

class ArmArch(PandaArch):
    registers: Incomplete
    reg_sp: Incomplete
    reg_pc: Incomplete
    reg_retaddr: Incomplete
    call_conventions: Incomplete
    reg_retval: Incomplete
    def get_return_value(self, cpu): ...
    def get_return_address(self, cpu): ...

class Aarch64Arch(PandaArch):
    reg_sp: Incomplete
    registers: Incomplete
    reg_retaddr: Incomplete
    call_conventions: Incomplete
    reg_retval: Incomplete
    arm32: Incomplete
    def get_pc(self, cpu): ...
    def get_return_value(self, cpu): ...
    def get_return_address(self, cpu): ...

class MipsArch(PandaArch):
    reg_sp: Incomplete
    reg_retaddr: Incomplete
    call_conventions: Incomplete
    reg_retval: Incomplete
    registers: Incomplete
    def get_reg(self, cpu, reg): ...
    def get_pc(self, cpu): ...
    def get_call_return(self, cpu): ...
    def get_return_address(self, cpu): ...

class Mips64Arch(MipsArch):
    reg_sp: Incomplete
    reg_retaddr: Incomplete
    call_conventions: Incomplete
    reg_retval: Incomplete
    registers: Incomplete

class PowerPCArch(PandaArch):
    reg_sp: Incomplete
    registers: Incomplete
    registers_crf: Incomplete
    def get_pc(self, cpu): ...
    def get_reg(self, cpu, reg): ...

class X86_64Arch(PandaArch):
    call_conventions: Incomplete
    reg_sp: Incomplete
    reg_retval: Incomplete
    registers: Incomplete
    reg_names_general: Incomplete
    reg_names_short: Incomplete
    reg_names_byte: Incomplete
    seg_names: Incomplete
    reg_names_mmr: Incomplete
    def get_return_value(self, cpu): ...
    def get_return_address(self, cpu): ...
    def get_reg(self, cpu, reg): ...
    def set_reg(self, cpu, reg, val): ...

class X86Arch(X86_64Arch):
    reg_retval: Incomplete
    call_conventions: Incomplete
    reg_sp: Incomplete
    registers: Incomplete
