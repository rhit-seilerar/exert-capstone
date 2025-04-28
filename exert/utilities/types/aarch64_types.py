from enum import IntEnum
from collections.abc import Callable
import ctypes
class ARMGenericTimer:
    cval: int
    ctl: int

class AccelState:
    parent_obj: 'Object'

class Addr:
    typ: 'AddrType'
    val: int
    off: int
    flag: 'AddrFlag'

class AddrFlag(IntEnum):
    FUNCARG = 3
    READLOG = 2
    EXCEPTION = 1
    IRRELEVANT = 5

class AddrRange:
    start: list[int]
    size: list[int]

class AddrType(IntEnum):
    ADDR_LAST = 10
    RET = 9
    CONST = 8
    UNK = 7
    GSPEC = 6
    GREG = 5
    LADDR = 4
    PADDR = 3
    IADDR = 2
    MADDR = 1
    HADDR = 0

class AddressSpace:
    rcu: 'rcu_head'
    name: bytes
    root: 'MemoryRegion'
    ref_count: int
    malloced: bool
    current_map: 'FlatView'
    ioeventfd_nb: int
    ioeventfds: 'MemoryRegionIoeventfd'
    dispatch: 'AddressSpaceDispatch'
    next_dispatch: 'AddressSpaceDispatch'
    dispatch_listener: 'MemoryListener'
    listeners: 'memory_listeners_as'
    class internal_7:
        tqe_next: 'AddressSpace'
        tqe_prev: 'AddressSpace'

    address_spaces_link: internal_7

BlockCompletionFunc: None
class BusState:
    obj: 'Object'
    parent: 'DeviceState'
    name: bytes
    hotplug_handler: 'HotplugHandler'
    max_index: int
    realized: bool
    children: 'ChildrenHead'
    class internal_21:
        le_next: 'BusState'
        le_prev: 'BusState'

    sibling: internal_21

class CPUARMState:
    regs: list[int]
    xregs: list[int]
    pc: int
    pstate: int
    aarch64: int
    uncached_cpsr: int
    spsr: int
    banked_spsr: list[int]
    banked_r13: list[int]
    banked_r14: list[int]
    usr_regs: list[int]
    fiq_regs: list[int]
    CF: int
    VF: int
    NF: int
    ZF: int
    QF: int
    GE: int
    thumb: int
    condexec_bits: int
    daif: int
    elr_el: list[int]
    sp_el: list[int]
    class internal_22:
        c0_cpuid: int
        _unused_csselr0: int
        csselr_ns: int
        _unused_csselr1: int
        csselr_s: int
        csselr_el: list[int]
        _unused_sctlr: int
        sctlr_ns: int
        hsctlr: int
        sctlr_s: int
        sctlr_el: list[int]
        cpacr_el1: int
        cptr_el: list[int]
        c1_xscaleauxcr: int
        sder: int
        nsacr: int
        _unused_ttbr0_0: int
        ttbr0_ns: int
        _unused_ttbr0_1: int
        ttbr0_s: int
        ttbr0_el: list[int]
        _unused_ttbr1_0: int
        ttbr1_ns: int
        _unused_ttbr1_1: int
        ttbr1_s: int
        ttbr1_el: list[int]
        vttbr_el2: int
        tcr_el: list['TCR']
        vtcr_el2: 'TCR'
        c2_data: int
        c2_insn: int
        dacr_ns: int
        dacr_s: int
        dacr32_el2: int
        pmsav5_data_ap: int
        pmsav5_insn_ap: int
        hcr_el2: int
        scr_el3: int
        ifsr_ns: int
        ifsr_s: int
        ifsr32_el2: int
        _unused_dfsr: int
        dfsr_ns: int
        hsr: int
        dfsr_s: int
        esr_el: list[int]
        c6_region: list[int]
        _unused_far0: int
        dfar_ns: int
        ifar_ns: int
        dfar_s: int
        ifar_s: int
        _unused_far3: int
        far_el: list[int]
        hpfar_el2: int
        hstr_el2: int
        _unused_par_0: int
        par_ns: int
        _unused_par_1: int
        par_s: int
        par_el: list[int]
        c6_rgnr: int
        c9_insn: int
        c9_data: int
        c9_pmcr: int
        c9_pmcnten: int
        c9_pmovsr: int
        c9_pmuserenr: int
        c9_pmselr: int
        c9_pminten: int
        _unused_mair_0: int
        mair0_ns: int
        mair1_ns: int
        _unused_mair_1: int
        mair0_s: int
        mair1_s: int
        mair_el: list[int]
        _unused_vbar: int
        vbar_ns: int
        hvbar: int
        vbar_s: int
        vbar_el: list[int]
        mvbar: int
        fcseidr_ns: int
        fcseidr_s: int
        _unused_contextidr_0: int
        contextidr_ns: int
        _unused_contextidr_1: int
        contextidr_s: int
        contextidr_el: list[int]
        tpidrurw_ns: int
        tpidrprw_ns: int
        htpidr: int
        _tpidr_el3: int
        tpidr_el: list[int]
        tpidrurw_s: int
        tpidrprw_s: int
        tpidruro_s: int
        tpidruro_ns: int
        tpidrro_el: list[int]
        c14_cntfrq: int
        c14_cntkctl: int
        cnthctl_el2: int
        cntvoff_el2: int
        c14_timer: list['ARMGenericTimer']
        c15_cpar: int
        c15_ticonfig: int
        c15_i_max: int
        c15_i_min: int
        c15_threadid: int
        c15_config_base_address: int
        c15_diagnostic: int
        c15_power_diagnostic: int
        c15_power_control: int
        dbgbvr: list[int]
        dbgbcr: list[int]
        dbgwvr: list[int]
        dbgwcr: list[int]
        mdscr_el1: int
        oslsr_el1: int
        mdcr_el2: int
        mdcr_el3: int
        c15_ccnt: int
        pmccfiltr_el0: int
        vpidr_el2: int
        vmpidr_el2: int

    cp15: internal_22
    class internal_53:
        other_sp: int
        vecbase: int
        basepri: int
        control: int
        ccr: int
        cfsr: int
        hfsr: int
        dfsr: int
        mmfar: int
        bfar: int
        exception: int

    v7m: internal_53
    class internal_54:
        syndrome: int
        fsr: int
        vaddress: int
        target_el: int

    exception: internal_54
    teecr: int
    teehbr: int
    class internal_55:
        regs: list[int]
        xregs: list[int]
        vec_len: int
        vec_stride: int
        scratch: list[int]
        fp_status: 'float_status'
        standard_fp_status: 'float_status'

    vfp: internal_55
    exclusive_addr: int
    exclusive_val: int
    exclusive_high: int
    class internal_56:
        regs: list[int]
        val: int
        cregs: list[int]

    iwmmxt: internal_56
    cpu_breakpoint: list['CPUBreakpoint']
    cpu_watchpoint: list['CPUWatchpoint']
    tlb_table: list[list['CPUTLBEntry']]
    tlb_v_table: list[list['CPUTLBEntry']]
    iotlb: list[list['CPUIOTLBEntry']]
    iotlb_v: list[list['CPUIOTLBEntry']]
    tlb_flush_addr: int
    tlb_flush_mask: int
    vtlb_index: int
    features: int
    class internal_57:
        drbar: int
        drsr: int
        dracr: int

    pmsav7: internal_57
    nvic: ctypes.c_void_p
    boot_info: 'arm_boot_info'
    gicv3state: ctypes.c_void_p

class CPUAddressSpace:
    cpu: 'CPUState'
    memory_dispatch: 'AddressSpaceDispatch'
    tcg_as_listener: 'MemoryListener'

CPUArchIdList: int
class CPUBreakpoint:
    pc: int
    rr_instr_count: int
    flags: int
    entry: 'CPUBreakpoint_qtailq'

class CPUBreakpoint_qtailq:
    tqe_next: 'CPUBreakpoint'
    tqe_prev: 'CPUBreakpoint'

class CPUIOTLBEntry:
    addr: int
    attrs: 'MemTxAttrs'

CPUReadMemoryFunc: int
class CPUState:
    parent_obj: 'DeviceState'
    nr_cores: int
    nr_threads: int
    numa_node: int
    thread: 'QemuThread'
    thread_id: int
    host_tid: int
    running: bool
    has_waiter: bool
    halt_cond: 'QemuCond'
    thread_kicked: bool
    created: bool
    stop: bool
    stopped: bool
    unplug: bool
    crash_occurred: bool
    exit_request: bool
    interrupt_request: int
    singlestep_enabled: int
    icount_budget: int
    icount_extra: int
    jmp_env: list[int]
    work_mutex: 'QemuMutex'
    queued_work_first: 'qemu_work_item'
    queued_work_last: 'qemu_work_item'
    cpu_ases: 'CPUAddressSpace'
    num_ases: int
    memory: 'MemoryRegion'
    env_ptr: 'CPUARMState'
    tb_jmp_cache: list['TranslationBlock']
    gdb_regs: 'GDBRegisterState'
    gdb_num_regs: int
    gdb_num_g_regs: int
    class internal_58:
        tqe_next: 'CPUState'
        tqe_prev: 'CPUState'

    node: internal_58
    breakpoints: 'breakpoints_head'
    watchpoints: 'watchpoints_head'
    watchpoint_hit: 'CPUWatchpoint'
    watchpoints_disabled: bool
    opaque: ctypes.c_void_p
    mem_io_pc: int
    mem_io_vaddr: int
    kvm_fd: int
    kvm_vcpu_dirty: bool
    kvm_state: 'KVMState'
    kvm_run: 'kvm_run'
    trace_dstate: int
    cpu_index: int
    halted: int
    class internal_59:
        u32: int
        u16: 'icount_decr_u16'

    icount_decr: internal_59
    can_do_io: int
    exception_index: int
    rr_guest_instr_count: int
    panda_guest_pc: int
    reverse_flags: int
    last_gdb_instr: int
    last_bp_hit_instr: int
    temp_rr_bp_instr: int
    throttle_thread_scheduled: bool
    tcg_exit_req: int
    hax_vcpu_dirty: bool
    hax_vcpu: 'hax_vcpu_state'
    pending_tlb_flush: int

class CPUTLBEntry:
    addr_read: int
    addr_write: int
    addr_code: int
    addend: int
    dummy: list[int]

class CPUWatchpoint:
    virtaddr: int
    len: int
    hitaddr: int
    hitattrs: 'MemTxAttrs'
    flags: int
    class internal_6:
        tqe_next: 'CPUWatchpoint'
        tqe_prev: 'CPUWatchpoint'

    entry: internal_6

CPUWriteMemoryFunc: None
class CharBackend:
    chr: 'Chardev'
    chr_event: Callable[[ctypes.c_void_p, int], None]
    chr_can_read: Callable[[ctypes.c_void_p], int]
    chr_read: Callable[[ctypes.c_void_p, int, int], None]
    opaque: ctypes.c_void_p
    tag: int
    fe_open: int

class Chardev:
    parent_obj: 'Object'
    chr_write_lock: 'QemuMutex'
    be: 'CharBackend'
    label: bytes
    filename: bytes
    logfd: int
    be_open: int
    fd_in_tag: int
    features: list[int]
    class internal_18:
        tqe_next: 'Chardev'
        tqe_prev: 'Chardev'

    next: internal_18

class ChildrenHead:
    tqh_first: 'BusChild'
    tqh_last: 'BusChild'

Const: int
class CosiFile:
    addr: int
    file_struct: 'File'
    name: 'String'
    fd: int

class CosiFiles:
    pass

class CosiMappings:
    modules: 'Vec_CosiModule'

class CosiModule:
    modd: int
    base: int
    size: int
    vma: 'VmAreaStruct'
    file: 'String'
    name: 'String'

class CosiProc:
    addr: int
    task: 'TaskStruct'
    name: 'String'
    ppid: int
    mm: 'MmStruct'
    asid: int
    taskd: int

class CosiThread:
    tid: int
    pid: int

class DeviceState:
    parent_obj: 'Object'
    id: bytes
    realized: bool
    pending_deleted_event: bool
    opts: 'QemuOpts'
    hotplugged: int
    parent_bus: 'BusState'
    class internal_16:
        lh_first: 'NamedGPIOList'

    gpios: internal_16
    class internal_17:
        lh_first: 'BusState'

    child_bus: internal_17
    num_child_bus: int
    instance_id_alias: int
    alias_required_for_version: int

class EventNotifier:
    rfd: int
    wfd: int

class FILE:
    pass

FPReg: list[int]
FeatureWordArray: list[int]
class File:
    f_path: 'Path'
    f_pos: int

GArray: None
class GDBRegisterState:
    base_reg: int
    num_regs: int
    get_reg: int
    set_reg: int
    xml: bytes
    next: 'GDBRegisterState'

class GHashTable:
    pass

GReg: int
GSpec: int
HAddr: int
class HotplugHandler:
    Parent: 'Object'

IAddr: int
IOCanReadHandler: int
IOEventHandler: None
class IOMMUAccessFlags(IntEnum):
    IOMMU_RW = 3
    IOMMU_WO = 2
    IOMMU_RO = 1
    IOMMU_NONE = 0

class IOMMUNotifierFlag(IntEnum):
    IOMMU_NOTIFIER_MAP = 2
    IOMMU_NOTIFIER_UNMAP = 1
    IOMMU_NOTIFIER_NONE = 0

class IOMMUTLBEntry:
    target_as: 'AddressSpace'
    iova: int
    translated_addr: int
    addr_mask: int
    perm: 'IOMMUAccessFlags'

IOReadHandler: None
class InsnFlag(IntEnum):
    INSNREADLOG = 1

Int128: list[int]
LAddr: int
class ListHead:
    next: int
    prev: int

class Location:
    num: int
    ptr: ctypes.c_void_p
    prev: 'Location'

MAddr: int
MMXReg: list[int]
class MTRRVar:
    base: int
    mask: int

class MachineState:
    parent_obj: 'Object'
    sysbus_notifier: 'Notifier'
    accel: bytes
    kernel_irqchip_allowed: bool
    kernel_irqchip_required: bool
    kernel_irqchip_split: bool
    kvm_shadow_mem: int
    dtb: bytes
    dumpdtb: bytes
    phandle_start: int
    dt_compatible: bytes
    dump_guest_core: bool
    mem_merge: bool
    usb: bool
    usb_disabled: bool
    igd_gfx_passthru: bool
    firmware: bytes
    iommu: bool
    suppress_vmdesc: bool
    enforce_config_section: bool
    enable_graphics: bool
    board_id: int
    mem_map_str: bytes
    ram_size: int
    maxram_size: int
    ram_slots: int
    boot_order: bytes
    kernel_filename: bytes
    kernel_cmdline: bytes
    initrd_filename: bytes
    cpu_model: bytes
    accelerator: 'AccelState'
    possible_cpus: int

class MemTxAttrs:
    unspecified: int
    secure: int
    user: int
    requester_id: int

MemTxResult: int
class MemoryListener:
    begin: Callable[['MemoryListener'], None]
    commit: Callable[['MemoryListener'], None]
    region_add: Callable[['MemoryListener', 'MemoryRegionSection'], None]
    region_del: Callable[['MemoryListener', 'MemoryRegionSection'], None]
    region_nop: Callable[['MemoryListener', 'MemoryRegionSection'], None]
    log_start: Callable[['MemoryListener', 'MemoryRegionSection', int, int], None]
    log_stop: Callable[['MemoryListener', 'MemoryRegionSection', int, int], None]
    log_sync: Callable[['MemoryListener', 'MemoryRegionSection'], None]
    log_global_start: Callable[['MemoryListener'], None]
    log_global_stop: Callable[['MemoryListener'], None]
    eventfd_add: Callable[['MemoryListener', 'MemoryRegionSection', bool, int, 'EventNotifier'], None]
    eventfd_del: Callable[['MemoryListener', 'MemoryRegionSection', bool, int, 'EventNotifier'], None]
    coalesced_mmio_add: Callable[['MemoryListener', 'MemoryRegionSection', int, int], None]
    coalesced_mmio_del: Callable[['MemoryListener', 'MemoryRegionSection', int, int], None]
    priority: int
    address_space: 'AddressSpace'
    class internal_13:
        tqe_next: 'MemoryListener'
        tqe_prev: 'MemoryListener'

    link: internal_13
    class internal_14:
        tqe_next: 'MemoryListener'
        tqe_prev: 'MemoryListener'

    link_as: internal_14

class MemoryRegion:
    parent_obj: 'Object'
    romd_mode: bool
    ram: bool
    subpage: bool
    readonly: bool
    rom_device: bool
    flush_coalesced_mmio: bool
    global_locking: bool
    dirty_log_mask: int
    ram_block: 'RAMBlock'
    owner: 'Object'
    iommu_ops: 'MemoryRegionIOMMUOps'
    ops: 'MemoryRegionOps'
    opaque: ctypes.c_void_p
    container: 'MemoryRegion'
    size: list[int]
    addr: int
    destructor: Callable[['MemoryRegion'], None]
    align: int
    terminates: bool
    ram_device: bool
    enabled: bool
    warning_printed: bool
    vga_logging_count: int
    alias: 'MemoryRegion'
    alias_offset: int
    priority: int
    subregions: 'subregions'
    class internal_11:
        tqe_next: 'MemoryRegion'
        tqe_prev: 'MemoryRegion'

    subregions_link: internal_11
    coalesced: 'coalesced_ranges'
    name: bytes
    ioeventfd_nb: int
    ioeventfds: 'MemoryRegionIoeventfd'
    class internal_12:
        lh_first: 'IOMMUNotifier'

    iommu_notify: internal_12
    iommu_notify_flags: 'IOMMUNotifierFlag'

class MemoryRegionIOMMUOps:
    translate: Callable[['MemoryRegion', int, bool], 'IOMMUTLBEntry']
    get_min_page_size: Callable[['MemoryRegion'], int]
    notify_flag_changed: Callable[['MemoryRegion', 'IOMMUNotifierFlag', 'IOMMUNotifierFlag'], None]

class MemoryRegionIoeventfd:
    addr: 'AddrRange'
    match_data: bool
    data: int
    e: 'EventNotifier'

class MemoryRegionMmio:
    read: list[Callable[[ctypes.c_void_p, int], int]]
    write: list[Callable[[ctypes.c_void_p, int, int], None]]

class MemoryRegionOps:
    read: Callable[[ctypes.c_void_p, int, int], int]
    write: Callable[[ctypes.c_void_p, int, int, int], None]
    read_with_attrs: Callable[[ctypes.c_void_p, int, int, int, 'MemTxAttrs'], int]
    write_with_attrs: Callable[[ctypes.c_void_p, int, int, int, 'MemTxAttrs'], int]
    endianness: 'device_endian'
    class internal_9:
        min_access_size: int
        max_access_size: int
        unaligned: bool
        accepts: Callable[[ctypes.c_void_p, int, int, bool], bool]

    valid: internal_9
    class internal_10:
        min_access_size: int
        max_access_size: int
        unaligned: bool

    impl: internal_10
    old_mmio: 'MemoryRegionMmio'

class MemoryRegionSection:
    mr: 'MemoryRegion'
    address_space: 'AddressSpace'
    offset_within_region: int
    size: list[int]
    offset_within_address_space: int
    readonly: bool

class MmStruct:
    pgd: int
    arg_start: int
    start_brk: int
    brk: int
    start_stack: int
    mmap: int

class Monitor:
    chr: 'CharBackend'
    reset_seen: int
    flags: int
    suspend_cnt: int
    skip_flush: bool
    out_lock: 'QemuMutex'
    outbuf: 'QString'
    out_watch: int
    mux_out: int
    rs: 'ReadLineState'
    qmp: list[int]
    mon_cpu: 'CPUState'
    password_completion_cb: Callable[[ctypes.c_void_p, int], None]
    password_opaque: ctypes.c_void_p
    cmd_table: list[int]
    class internal_19:
        lh_first: 'mon_fd_t'

    fds: internal_19
    class internal_20:
        le_next: 'Monitor'
        le_prev: 'Monitor'

    entry: internal_20

MonitorQMP: list[int]
class Notifier:
    notify: Callable[['Notifier', ctypes.c_void_p], None]
    class internal_3:
        le_next: 'Notifier'
        le_prev: 'Notifier'

    node: internal_3

class Object:
    klass: ctypes.c_void_p
    free: ctypes.c_void_p
    properties: ctypes.c_void_p
    ref: int
    parent: ctypes.c_void_p

class OsiModule:
    modd: int
    base: int
    size: int
    file: bytes
    name: bytes
    offset: int
    flags: int

class OsiPage:
    start: int
    len: int

class OsiProc:
    taskd: int
    pgd: int
    asid: int
    pid: int
    ppid: int
    name: bytes
    pages: 'osi_page_struct'
    create_time: int

class OsiProcHandle:
    taskd: int
    asid: int

class OsiProcMem:
    start_brk: int
    brk: int

class OsiThread:
    pid: int
    tid: int

PAddr: int
class PandaOsFamily(IntEnum):
    OS_FREEBSD = 3
    OS_LINUX = 2
    OS_WINDOWS = 1
    OS_UNKNOWN = 0

class Path:
    dentry: int
    mnt: int

QDict: list[int]
QEMUClockType: int
QEMUTimerCB: None
QEMUTimerListNotifyCB: None
class QObject:
    type: int
    refcnt: int

class QString:
    base: 'QObject'
    string: bytes
    length: int
    capacity: int

QType: int
class QemuCond:
    cond: list[int]

class QemuMutex:
    lock: list[int]

class QemuOptDesc:
    name: bytes
    type: 'QemuOptType'
    help: bytes
    def_value_str: bytes

class QemuOptHead:
    tqh_first: 'QemuOpt'
    tqh_last: 'QemuOpt'

class QemuOpts:
    id: bytes
    list: 'QemuOptsList'
    loc: 'Location'
    head: 'QemuOptHead'
    class internal_15:
        tqe_next: 'QemuOpts'
        tqe_prev: 'QemuOpts'

    next: internal_15

class QemuOptsList:
    name: bytes
    implied_opt_name: bytes
    merge_lists: bool
    class internal_8:
        tqh_first: 'QemuOpts'
        tqh_last: 'QemuOpts'

    head: internal_8
    desc: list['QemuOptDesc']

class QemuThread:
    thread: int

class QueryResult:
    num_labels: int
    ls: ctypes.c_void_p
    it_end: ctypes.c_void_p
    it_curr: ctypes.c_void_p
    tcn: int
    cb_mask: int

class RAMBlock:
    rcu: 'rcu_head'
    mr: 'MemoryRegion'
    host: int
    offset: int
    used_length: int
    max_length: int
    resized: Callable[[bytes, int, ctypes.c_void_p], None]
    flags: int
    idstr: list[bytes]
    class internal_1:
        le_next: 'RAMBlock'
        le_prev: 'RAMBlock'

    next: internal_1
    class internal_2:
        lh_first: 'RAMBlockNotifier'

    ramblock_notifiers: internal_2
    fd: int
    page_size: int

RCUCBFunc: None
class RRCTRL_ret(IntEnum):
    RRCTRL_OK = 0
    RRCTRL_EPENDING = -1
    RRCTRL_EINVALID = -2

class RR_mem_type(IntEnum):
    RR_MEM_UNKNOWN = 2
    RR_MEM_RAM = 1
    RR_MEM_IO = 0

class RR_mode(IntEnum):
    RR_REPLAY = 2
    RR_RECORD = 1
    RR_OFF = 0
    RR_NOCHANGE = -1

ReadLineCompletionFunc: None
ReadLineFlushFunc: None
ReadLineFunc: None
ReadLinePrintfFunc: None
class ReadLineState:
    cmd_buf: list[bytes]
    cmd_buf_index: int
    cmd_buf_size: int
    last_cmd_buf: list[bytes]
    last_cmd_buf_index: int
    last_cmd_buf_size: int
    esc_state: int
    esc_param: int
    history: list[bytes]
    hist_entry: int
    completion_finder: Callable[[ctypes.c_void_p, bytes], None]
    completions: list[bytes]
    nb_completions: int
    completion_index: int
    readline_func: Callable[[ctypes.c_void_p, bytes, ctypes.c_void_p], None]
    readline_opaque: ctypes.c_void_p
    read_password: int
    prompt: list[bytes]
    printf_func: Callable[[ctypes.c_void_p, bytes], None]
    flush_func: Callable[[ctypes.c_void_p], None]
    opaque: ctypes.c_void_p

Ret: int
class String:
    pass

class SymbolicBranchMeta:
    pc: int

TCGMemOp: int
class TCR:
    raw_tcr: int
    mask: int
    base_mask: int

class TPRAccess(IntEnum):
    TPR_ACCESS_WRITE = 1
    TPR_ACCESS_READ = 0

TaintLabel: int
class TaskStruct:
    tasks: 'ListHead'
    pid: int
    tgid: int
    group_leader: int
    thread_group: int
    real_parent: int
    parent: int
    mm: int
    stack: int
    real_cred: int
    cred: int
    comm: list[int]
    files: int
    start_time: int
    children: 'ListHead'
    sibling: 'ListHead'

class TranslationBlock:
    pc: int
    cs_base: int
    flags: int
    size: int
    icount: int
    cflags: int
    invalid: int
    was_split: int
    tc_ptr: ctypes.c_void_p
    tc_search: int
    orig_tb: 'TranslationBlock'
    page_next: list['TranslationBlock']
    page_addr: list[int]
    jmp_reset_offset: list[int]
    jmp_insn_offset: list[int]
    jmp_list_next: list[int]
    jmp_list_first: int
    llvm_tc_ptr: int
    llvm_tc_end: int
    llvm_tb_next: list['TranslationBlock']
    llvm_asm_ptr: int
    llvm_fn_name: list[bytes]

Unk: int
ValueUnion: int
class Vec_CosiModule:
    pass

class Vec_CosiProc:
    pass

class VmAreaStruct:
    vm_mm: int
    vm_start: int
    vm_end: int
    vm_next: int
    vm_file: int
    vm_flags: int

class VolatilityBaseType:
    pass

class VolatilityEnum:
    pass

class VolatilityStruct:
    pass

class VolatilitySymbol:
    pass

ZMMReg: list[int]
__u16: int
__u32: int
__u64: int
__u8: int
_add_hooks2_t: Callable[[Callable[['CPUState', 'TranslationBlock', ctypes.c_void_p], bool], ctypes.c_void_p, bool, bytes, bytes, int, int, int, int], int]
_disable_hooks2_t: Callable[[int], None]
_enable_hooks2_t: Callable[[int], None]
class breakpoints_head:
    tqh_first: 'CPUBreakpoint'
    tqh_last: 'CPUBreakpoint'

class coalesced_ranges:
    tqh_first: 'CoalescedMemoryRange'
    tqh_last: 'CoalescedMemoryRange'

dcr_read_cb: Callable[[ctypes.c_void_p, int], int]
dcr_write_cb: Callable[[ctypes.c_void_p, int, int], None]
dynamic_hook_func_t: Callable[['hook_symbol_resolve', 'symbol', int], None]
dynamic_symbol_hook_func_t: Callable[['CPUState', 'TranslationBlock', 'hook'], bool]
flag: bytes
float32: int
float64: int
class float_status:
    float_detect_tininess: int
    float_rounding_mode: int
    float_exception_flags: int
    floatx80_rounding_precision: int
    flush_to_zero: bytes
    flush_inputs_to_zero: bytes
    default_nan_mode: bytes
    snan_bit_is_one: bytes

class floatx80:
    low: int
    high: int

fpr_t: list[int]
gchar: bytes
gdb_reg_cb: int
guint: int
hax_fd: int
class hax_global:
    pass

class hax_vcpu_state:
    fd: int
    vcpu_id: int
    tunnel: 'hax_tunnel'
    iobuf: int

class hook:
    addr: int
    asid: int
    type: 'panda_cb_type'
    cb: 'hooks_panda_cb'
    km: 'kernel_mode'
    enabled: bool
    sym: 'symbol'
    context: ctypes.c_void_p

hook_func_t: Callable[['CPUState', 'TranslationBlock', 'hook'], bool]
hooks2_func_t: Callable[['CPUState', 'TranslationBlock', ctypes.c_void_p], bool]
class hooks_panda_cb:
    before_tcg_codegen: Callable[['CPUState', 'TranslationBlock', 'hook'], None]
    before_block_translate: Callable[['CPUState', int, 'hook'], None]
    after_block_translate: Callable[['CPUState', 'TranslationBlock', 'hook'], None]
    before_block_exec_invalidate_opt: Callable[['CPUState', 'TranslationBlock', 'hook'], bool]
    before_block_exec: Callable[['CPUState', 'TranslationBlock', 'hook'], None]
    after_block_exec: Callable[['CPUState', 'TranslationBlock', int, 'hook'], None]
    start_block_exec: Callable[['CPUState', 'TranslationBlock', 'hook'], None]
    end_block_exec: Callable[['CPUState', 'TranslationBlock', 'hook'], None]

hwaddr: int
hypercall_t: Callable[['CPUState'], None]
class icount_decr_u16:
    low: int
    high: int

mem_hook_func_t: Callable[['CPUState', 'memory_access_desc'], None]
class memory_listeners_as:
    tqh_first: 'MemoryListener'
    tqh_last: 'MemoryListener'

mon_cmd_t: list[int]
on_after_load_t: Callable[['addr_struct', int, int], None]
on_after_store_t: Callable[['addr_struct', int, int], None]
on_all_sys_enter2_t: Callable[['CPUState', int, 'syscall_info_t', 'syscall_ctx'], None]
on_all_sys_enter_t: Callable[['CPUState', int, int], None]
on_all_sys_return2_t: Callable[['CPUState', int, 'syscall_info_t', 'syscall_ctx'], None]
on_all_sys_return_t: Callable[['CPUState', int, int], None]
on_branch2_t: Callable[['addr_struct', int, bool, bool], None]
on_branch_t: Callable[['CPUState', 'TranslationBlock', int], bool]
on_call_match_num_t: Callable[['CPUState', int, int, int, int], None]
on_call_match_str_t: Callable[['CPUState', int, int, bytes, int, int], None]
on_call_t: Callable[['CPUState', int], None]
on_get_current_process_handle_t: Callable[['CPUState', 'osi_proc_handle_struct'], None]
on_get_current_process_t: Callable[['CPUState', 'osi_proc_struct'], None]
on_get_current_thread_t: Callable[['CPUState', 'osi_thread_struct'], None]
on_get_file_mappings_t: Callable[['CPUState', 'osi_proc_struct', ctypes.c_void_p], None]
on_get_heap_mappings_t: Callable[['CPUState', 'osi_proc_struct', ctypes.c_void_p], None]
on_get_mapping_base_address_by_name_t: Callable[['CPUState', 'osi_proc_struct', bytes, int], None]
on_get_mapping_by_addr_t: Callable[['CPUState', 'osi_proc_struct', int, 'osi_module_struct'], None]
on_get_mappings_t: Callable[['CPUState', 'osi_proc_struct', ctypes.c_void_p], None]
on_get_modules_t: Callable[['CPUState', ctypes.c_void_p], None]
on_get_proc_mem_t: Callable[['CPUState', 'osi_proc_struct', 'osi_proc_mem'], None]
on_get_process_handles_t: Callable[['CPUState', ctypes.c_void_p], None]
on_get_process_pid_t: Callable[['CPUState', 'osi_proc_handle_struct', int], None]
on_get_process_ppid_t: Callable[['CPUState', 'osi_proc_handle_struct', int], None]
on_get_process_t: Callable[['CPUState', 'osi_proc_handle_struct', 'osi_proc_struct'], None]
on_get_processes_t: Callable[['CPUState', ctypes.c_void_p], None]
on_get_stack_mappings_t: Callable[['CPUState', 'osi_proc_struct', ctypes.c_void_p], None]
on_get_unknown_mappings_t: Callable[['CPUState', 'osi_proc_struct', ctypes.c_void_p], None]
on_has_mapping_prefix_t: Callable[['CPUState', 'osi_proc_struct', bytes, bool], None]
on_indirect_jump_t: Callable[['addr_struct', int, bool, bool], None]
on_mmap_updated_t: Callable[['CPUState', bytes, int, int], None]
on_process_end_t: Callable[['CPUState', bytes, int, int], None]
on_process_start_t: Callable[['CPUState', bytes, int, int], None]
on_ptr_load_t: Callable[['addr_struct', int, int], None]
on_ptr_store_t: Callable[['addr_struct', int, int], None]
on_rec_auxv_t: Callable[['CPUState', 'TranslationBlock', 'auxv_values'], None]
on_ret_t: Callable[['CPUState', int], None]
on_ssm_t: Callable[['CPUState', int, int, int, int, bool, bool], None]
on_sys_accept4_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_accept4_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_accept_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_accept_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_acct_enter_t: Callable[['CPUState', int, int], None]
on_sys_acct_return_t: Callable[['CPUState', int, int], None]
on_sys_add_key_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_add_key_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_adjtimex_enter_t: Callable[['CPUState', int, int], None]
on_sys_adjtimex_return_t: Callable[['CPUState', int, int], None]
on_sys_bind_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_bind_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_bpf_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_bpf_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_brk_enter_t: Callable[['CPUState', int, int], None]
on_sys_brk_return_t: Callable[['CPUState', int, int], None]
on_sys_capget_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_capget_return_t: Callable[['CPUState', int, int, int], None]
on_sys_capset_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_capset_return_t: Callable[['CPUState', int, int, int], None]
on_sys_chdir_enter_t: Callable[['CPUState', int, int], None]
on_sys_chdir_return_t: Callable[['CPUState', int, int], None]
on_sys_chroot_enter_t: Callable[['CPUState', int, int], None]
on_sys_chroot_return_t: Callable[['CPUState', int, int], None]
on_sys_clock_adjtime_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_clock_adjtime_return_t: Callable[['CPUState', int, int, int], None]
on_sys_clock_getres_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_clock_getres_return_t: Callable[['CPUState', int, int, int], None]
on_sys_clock_gettime_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_clock_gettime_return_t: Callable[['CPUState', int, int, int], None]
on_sys_clock_nanosleep_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_clock_nanosleep_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_clock_settime_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_clock_settime_return_t: Callable[['CPUState', int, int, int], None]
on_sys_clone3_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_clone3_return_t: Callable[['CPUState', int, int, int], None]
on_sys_clone_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_clone_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_close_enter_t: Callable[['CPUState', int, int], None]
on_sys_close_return_t: Callable[['CPUState', int, int], None]
on_sys_connect_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_connect_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_copy_file_range_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_copy_file_range_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_delete_module_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_delete_module_return_t: Callable[['CPUState', int, int, int], None]
on_sys_dup3_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_dup3_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_dup_enter_t: Callable[['CPUState', int, int], None]
on_sys_dup_return_t: Callable[['CPUState', int, int], None]
on_sys_epoll_create1_enter_t: Callable[['CPUState', int, int], None]
on_sys_epoll_create1_return_t: Callable[['CPUState', int, int], None]
on_sys_epoll_ctl_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_epoll_ctl_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_epoll_pwait_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_epoll_pwait_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_eventfd2_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_eventfd2_return_t: Callable[['CPUState', int, int, int], None]
on_sys_execve_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_execve_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_execveat_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_execveat_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_exit_enter_t: Callable[['CPUState', int, int], None]
on_sys_exit_group_enter_t: Callable[['CPUState', int, int], None]
on_sys_exit_group_return_t: Callable[['CPUState', int, int], None]
on_sys_exit_return_t: Callable[['CPUState', int, int], None]
on_sys_faccessat2_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_faccessat2_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_faccessat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_faccessat_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_fadvise64_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_fadvise64_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_fallocate_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_fallocate_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_fanotify_init_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_fanotify_init_return_t: Callable[['CPUState', int, int, int], None]
on_sys_fanotify_mark_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_fanotify_mark_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_fchdir_enter_t: Callable[['CPUState', int, int], None]
on_sys_fchdir_return_t: Callable[['CPUState', int, int], None]
on_sys_fchmod_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_fchmod_return_t: Callable[['CPUState', int, int, int], None]
on_sys_fchmodat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_fchmodat_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_fchown_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_fchown_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_fchownat_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_fchownat_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_fcntl_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_fcntl_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_fdatasync_enter_t: Callable[['CPUState', int, int], None]
on_sys_fdatasync_return_t: Callable[['CPUState', int, int], None]
on_sys_fgetxattr_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_fgetxattr_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_finit_module_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_finit_module_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_flistxattr_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_flistxattr_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_flock_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_flock_return_t: Callable[['CPUState', int, int, int], None]
on_sys_fremovexattr_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_fremovexattr_return_t: Callable[['CPUState', int, int, int], None]
on_sys_fsetxattr_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_fsetxattr_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_fstat_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_fstat_return_t: Callable[['CPUState', int, int, int], None]
on_sys_fstatfs_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_fstatfs_return_t: Callable[['CPUState', int, int, int], None]
on_sys_fsync_enter_t: Callable[['CPUState', int, int], None]
on_sys_fsync_return_t: Callable[['CPUState', int, int], None]
on_sys_ftruncate_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_ftruncate_return_t: Callable[['CPUState', int, int, int], None]
on_sys_futex_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_futex_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_get_mempolicy_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_get_mempolicy_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_get_robust_list_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_get_robust_list_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getcpu_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getcpu_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getcwd_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_getcwd_return_t: Callable[['CPUState', int, int, int], None]
on_sys_getdents64_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getdents64_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getegid_enter_t: Callable[['CPUState', int], None]
on_sys_getegid_return_t: Callable[['CPUState', int], None]
on_sys_geteuid_enter_t: Callable[['CPUState', int], None]
on_sys_geteuid_return_t: Callable[['CPUState', int], None]
on_sys_getgid_enter_t: Callable[['CPUState', int], None]
on_sys_getgid_return_t: Callable[['CPUState', int], None]
on_sys_getgroups_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_getgroups_return_t: Callable[['CPUState', int, int, int], None]
on_sys_getitimer_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_getitimer_return_t: Callable[['CPUState', int, int, int], None]
on_sys_getpeername_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getpeername_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getpgid_enter_t: Callable[['CPUState', int, int], None]
on_sys_getpgid_return_t: Callable[['CPUState', int, int], None]
on_sys_getpid_enter_t: Callable[['CPUState', int], None]
on_sys_getpid_return_t: Callable[['CPUState', int], None]
on_sys_getppid_enter_t: Callable[['CPUState', int], None]
on_sys_getppid_return_t: Callable[['CPUState', int], None]
on_sys_getpriority_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_getpriority_return_t: Callable[['CPUState', int, int, int], None]
on_sys_getrandom_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getrandom_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getresgid_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getresgid_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getresuid_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getresuid_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getrlimit_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_getrlimit_return_t: Callable[['CPUState', int, int, int], None]
on_sys_getrusage_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_getrusage_return_t: Callable[['CPUState', int, int, int], None]
on_sys_getsid_enter_t: Callable[['CPUState', int, int], None]
on_sys_getsid_return_t: Callable[['CPUState', int, int], None]
on_sys_getsockname_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getsockname_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getsockopt_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_getsockopt_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_gettid_enter_t: Callable[['CPUState', int], None]
on_sys_gettid_return_t: Callable[['CPUState', int], None]
on_sys_gettimeofday_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_gettimeofday_return_t: Callable[['CPUState', int, int, int], None]
on_sys_getuid_enter_t: Callable[['CPUState', int], None]
on_sys_getuid_return_t: Callable[['CPUState', int], None]
on_sys_getxattr_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_getxattr_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_init_module_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_init_module_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_inotify_add_watch_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_inotify_add_watch_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_inotify_init1_enter_t: Callable[['CPUState', int, int], None]
on_sys_inotify_init1_return_t: Callable[['CPUState', int, int], None]
on_sys_inotify_rm_watch_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_inotify_rm_watch_return_t: Callable[['CPUState', int, int, int], None]
on_sys_io_cancel_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_io_cancel_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_io_destroy_enter_t: Callable[['CPUState', int, int], None]
on_sys_io_destroy_return_t: Callable[['CPUState', int, int], None]
on_sys_io_getevents_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_io_getevents_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_io_setup_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_io_setup_return_t: Callable[['CPUState', int, int, int], None]
on_sys_io_submit_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_io_submit_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_ioctl_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_ioctl_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_ioprio_get_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_ioprio_get_return_t: Callable[['CPUState', int, int, int], None]
on_sys_ioprio_set_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_ioprio_set_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_kcmp_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_kcmp_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_kexec_file_load_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_kexec_file_load_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_kexec_load_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_kexec_load_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_keyctl_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_keyctl_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_kill_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_kill_return_t: Callable[['CPUState', int, int, int], None]
on_sys_lgetxattr_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_lgetxattr_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_linkat_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_linkat_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_listen_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_listen_return_t: Callable[['CPUState', int, int, int], None]
on_sys_listxattr_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_listxattr_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_llistxattr_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_llistxattr_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_lookup_dcookie_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_lookup_dcookie_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_lremovexattr_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_lremovexattr_return_t: Callable[['CPUState', int, int, int], None]
on_sys_lseek_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_lseek_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_lsetxattr_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_lsetxattr_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_madvise_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_madvise_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_mbind_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_mbind_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_membarrier_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_membarrier_return_t: Callable[['CPUState', int, int, int], None]
on_sys_memfd_create_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_memfd_create_return_t: Callable[['CPUState', int, int, int], None]
on_sys_migrate_pages_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_migrate_pages_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_mincore_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_mincore_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_mkdirat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_mkdirat_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_mknodat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_mknodat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_mlock2_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_mlock2_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_mlock_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_mlock_return_t: Callable[['CPUState', int, int, int], None]
on_sys_mlockall_enter_t: Callable[['CPUState', int, int], None]
on_sys_mlockall_return_t: Callable[['CPUState', int, int], None]
on_sys_mmap_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_mmap_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_mount_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_mount_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_move_pages_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_move_pages_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_mprotect_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_mprotect_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_mq_getsetattr_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_mq_getsetattr_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_mq_notify_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_mq_notify_return_t: Callable[['CPUState', int, int, int], None]
on_sys_mq_open_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_mq_open_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_mq_timedreceive_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_mq_timedreceive_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_mq_timedsend_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_mq_timedsend_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_mq_unlink_enter_t: Callable[['CPUState', int, int], None]
on_sys_mq_unlink_return_t: Callable[['CPUState', int, int], None]
on_sys_mremap_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_mremap_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_msgctl_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_msgctl_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_msgget_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_msgget_return_t: Callable[['CPUState', int, int, int], None]
on_sys_msgrcv_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_msgrcv_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_msgsnd_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_msgsnd_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_msync_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_msync_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_munlock_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_munlock_return_t: Callable[['CPUState', int, int, int], None]
on_sys_munlockall_enter_t: Callable[['CPUState', int], None]
on_sys_munlockall_return_t: Callable[['CPUState', int], None]
on_sys_munmap_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_munmap_return_t: Callable[['CPUState', int, int, int], None]
on_sys_name_to_handle_at_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_name_to_handle_at_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_nanosleep_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_nanosleep_return_t: Callable[['CPUState', int, int, int], None]
on_sys_newfstatat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_newfstatat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_nfsservctl_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_nfsservctl_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_open_by_handle_at_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_open_by_handle_at_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_openat2_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_openat2_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_openat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_openat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_perf_event_open_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_perf_event_open_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_personality_enter_t: Callable[['CPUState', int, int], None]
on_sys_personality_return_t: Callable[['CPUState', int, int], None]
on_sys_pidfd_getfd_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_pidfd_getfd_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_pidfd_open_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_pidfd_open_return_t: Callable[['CPUState', int, int, int], None]
on_sys_pidfd_send_signal_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_pidfd_send_signal_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_pipe2_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_pipe2_return_t: Callable[['CPUState', int, int, int], None]
on_sys_pivot_root_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_pivot_root_return_t: Callable[['CPUState', int, int, int], None]
on_sys_pkey_alloc_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_pkey_alloc_return_t: Callable[['CPUState', int, int, int], None]
on_sys_pkey_free_enter_t: Callable[['CPUState', int, int], None]
on_sys_pkey_free_return_t: Callable[['CPUState', int, int], None]
on_sys_pkey_mprotect_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_pkey_mprotect_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_ppoll_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_ppoll_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_prctl_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_prctl_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_pread64_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_pread64_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_preadv2_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_preadv2_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_preadv_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_preadv_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_prlimit64_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_prlimit64_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_process_vm_readv_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_process_vm_readv_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_process_vm_writev_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_process_vm_writev_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_pselect6_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_pselect6_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_ptrace_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_ptrace_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_pwrite64_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_pwrite64_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_pwritev2_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_pwritev2_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_pwritev_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_pwritev_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_quotactl_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_quotactl_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_read_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_read_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_readahead_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_readahead_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_readlinkat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_readlinkat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_readv_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_readv_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_reboot_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_reboot_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_recvfrom_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_recvfrom_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_recvmmsg_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_recvmmsg_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_recvmsg_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_recvmsg_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_remap_file_pages_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_remap_file_pages_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_removexattr_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_removexattr_return_t: Callable[['CPUState', int, int, int], None]
on_sys_renameat2_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_renameat2_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_renameat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_renameat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_request_key_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_request_key_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_restart_syscall_enter_t: Callable[['CPUState', int], None]
on_sys_restart_syscall_return_t: Callable[['CPUState', int], None]
on_sys_rt_sigaction_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_rt_sigaction_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_rt_sigpending_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_rt_sigpending_return_t: Callable[['CPUState', int, int, int], None]
on_sys_rt_sigprocmask_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_rt_sigprocmask_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_rt_sigqueueinfo_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_rt_sigqueueinfo_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_rt_sigreturn_enter_t: Callable[['CPUState', int, int], None]
on_sys_rt_sigreturn_return_t: Callable[['CPUState', int, int], None]
on_sys_rt_sigsuspend_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_rt_sigsuspend_return_t: Callable[['CPUState', int, int, int], None]
on_sys_rt_sigtimedwait_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_rt_sigtimedwait_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_rt_tgsigqueueinfo_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_rt_tgsigqueueinfo_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_sched_get_priority_max_enter_t: Callable[['CPUState', int, int], None]
on_sys_sched_get_priority_max_return_t: Callable[['CPUState', int, int], None]
on_sys_sched_get_priority_min_enter_t: Callable[['CPUState', int, int], None]
on_sys_sched_get_priority_min_return_t: Callable[['CPUState', int, int], None]
on_sys_sched_getaffinity_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_sched_getaffinity_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_sched_getattr_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_sched_getattr_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_sched_getparam_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_sched_getparam_return_t: Callable[['CPUState', int, int, int], None]
on_sys_sched_getscheduler_enter_t: Callable[['CPUState', int, int], None]
on_sys_sched_getscheduler_return_t: Callable[['CPUState', int, int], None]
on_sys_sched_rr_get_interval_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_sched_rr_get_interval_return_t: Callable[['CPUState', int, int, int], None]
on_sys_sched_setaffinity_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_sched_setaffinity_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_sched_setattr_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_sched_setattr_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_sched_setparam_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_sched_setparam_return_t: Callable[['CPUState', int, int, int], None]
on_sys_sched_setscheduler_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_sched_setscheduler_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_sched_yield_enter_t: Callable[['CPUState', int], None]
on_sys_sched_yield_return_t: Callable[['CPUState', int], None]
on_sys_seccomp_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_seccomp_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_semctl_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_semctl_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_semget_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_semget_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_semop_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_semop_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_semtimedop_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_semtimedop_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_sendfile_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_sendfile_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_sendmmsg_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_sendmmsg_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_sendmsg_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_sendmsg_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_sendto_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_sendto_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_set_mempolicy_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_set_mempolicy_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_set_robust_list_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_set_robust_list_return_t: Callable[['CPUState', int, int, int], None]
on_sys_set_tid_address_enter_t: Callable[['CPUState', int, int], None]
on_sys_set_tid_address_return_t: Callable[['CPUState', int, int], None]
on_sys_setdomainname_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_setdomainname_return_t: Callable[['CPUState', int, int, int], None]
on_sys_setfsgid_enter_t: Callable[['CPUState', int, int], None]
on_sys_setfsgid_return_t: Callable[['CPUState', int, int], None]
on_sys_setfsuid_enter_t: Callable[['CPUState', int, int], None]
on_sys_setfsuid_return_t: Callable[['CPUState', int, int], None]
on_sys_setgid_enter_t: Callable[['CPUState', int, int], None]
on_sys_setgid_return_t: Callable[['CPUState', int, int], None]
on_sys_setgroups_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_setgroups_return_t: Callable[['CPUState', int, int, int], None]
on_sys_sethostname_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_sethostname_return_t: Callable[['CPUState', int, int, int], None]
on_sys_setitimer_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_setitimer_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_setns_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_setns_return_t: Callable[['CPUState', int, int, int], None]
on_sys_setpgid_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_setpgid_return_t: Callable[['CPUState', int, int, int], None]
on_sys_setpriority_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_setpriority_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_setregid_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_setregid_return_t: Callable[['CPUState', int, int, int], None]
on_sys_setresgid_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_setresgid_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_setresuid_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_setresuid_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_setreuid_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_setreuid_return_t: Callable[['CPUState', int, int, int], None]
on_sys_setrlimit_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_setrlimit_return_t: Callable[['CPUState', int, int, int], None]
on_sys_setsid_enter_t: Callable[['CPUState', int], None]
on_sys_setsid_return_t: Callable[['CPUState', int], None]
on_sys_setsockopt_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_setsockopt_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_settimeofday_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_settimeofday_return_t: Callable[['CPUState', int, int, int], None]
on_sys_setuid_enter_t: Callable[['CPUState', int, int], None]
on_sys_setuid_return_t: Callable[['CPUState', int, int], None]
on_sys_setxattr_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_setxattr_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_shmat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_shmat_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_shmctl_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_shmctl_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_shmdt_enter_t: Callable[['CPUState', int, int], None]
on_sys_shmdt_return_t: Callable[['CPUState', int, int], None]
on_sys_shmget_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_shmget_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_shutdown_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_shutdown_return_t: Callable[['CPUState', int, int, int], None]
on_sys_sigaltstack_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_sigaltstack_return_t: Callable[['CPUState', int, int, int], None]
on_sys_signalfd4_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_signalfd4_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_socket_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_socket_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_socketpair_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_socketpair_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_splice_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_splice_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_statfs_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_statfs_return_t: Callable[['CPUState', int, int, int], None]
on_sys_statx_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_statx_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_swapoff_enter_t: Callable[['CPUState', int, int], None]
on_sys_swapoff_return_t: Callable[['CPUState', int, int], None]
on_sys_swapon_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_swapon_return_t: Callable[['CPUState', int, int, int], None]
on_sys_symlinkat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_symlinkat_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_sync_enter_t: Callable[['CPUState', int], None]
on_sys_sync_file_range_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_sync_file_range_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_sync_return_t: Callable[['CPUState', int], None]
on_sys_syncfs_enter_t: Callable[['CPUState', int, int], None]
on_sys_syncfs_return_t: Callable[['CPUState', int, int], None]
on_sys_sysinfo_enter_t: Callable[['CPUState', int, int], None]
on_sys_sysinfo_return_t: Callable[['CPUState', int, int], None]
on_sys_syslog_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_syslog_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_tee_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_tee_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_tgkill_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_tgkill_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_timer_create_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_timer_create_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_timer_delete_enter_t: Callable[['CPUState', int, int], None]
on_sys_timer_delete_return_t: Callable[['CPUState', int, int], None]
on_sys_timer_getoverrun_enter_t: Callable[['CPUState', int, int], None]
on_sys_timer_getoverrun_return_t: Callable[['CPUState', int, int], None]
on_sys_timer_gettime_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_timer_gettime_return_t: Callable[['CPUState', int, int, int], None]
on_sys_timer_settime_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_timer_settime_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_timerfd_create_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_timerfd_create_return_t: Callable[['CPUState', int, int, int], None]
on_sys_timerfd_gettime_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_timerfd_gettime_return_t: Callable[['CPUState', int, int, int], None]
on_sys_timerfd_settime_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_timerfd_settime_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_times_enter_t: Callable[['CPUState', int, int], None]
on_sys_times_return_t: Callable[['CPUState', int, int], None]
on_sys_tkill_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_tkill_return_t: Callable[['CPUState', int, int, int], None]
on_sys_truncate_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_truncate_return_t: Callable[['CPUState', int, int, int], None]
on_sys_umask_enter_t: Callable[['CPUState', int, int], None]
on_sys_umask_return_t: Callable[['CPUState', int, int], None]
on_sys_umount2_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_umount2_return_t: Callable[['CPUState', int, int, int], None]
on_sys_uname_enter_t: Callable[['CPUState', int, int], None]
on_sys_uname_return_t: Callable[['CPUState', int, int], None]
on_sys_unlinkat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_unlinkat_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_unshare_enter_t: Callable[['CPUState', int, int], None]
on_sys_unshare_return_t: Callable[['CPUState', int, int], None]
on_sys_userfaultfd_enter_t: Callable[['CPUState', int, int], None]
on_sys_userfaultfd_return_t: Callable[['CPUState', int, int], None]
on_sys_utimensat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_utimensat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_vhangup_enter_t: Callable[['CPUState', int], None]
on_sys_vhangup_return_t: Callable[['CPUState', int], None]
on_sys_vmsplice_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_vmsplice_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_wait4_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_wait4_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_waitid_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_waitid_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_write_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_write_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_writev_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_writev_return_t: Callable[['CPUState', int, int, int, int], None]
on_taint_change_t: Callable[['addr_struct', int], None]
on_taint_prop_t: Callable[['addr_struct', 'addr_struct', int], None]
on_task_change_t: Callable[['CPUState'], None]
on_thread_end_t: Callable[['CPUState', bytes, int, int, int], None]
on_thread_start_t: Callable[['CPUState', bytes, int, int, int], None]
on_unknown_sys_enter_t: Callable[['CPUState', int, int], None]
on_unknown_sys_return_t: Callable[['CPUState', int, int], None]
class panda_arg:
    argptr: bytes
    key: bytes
    value: bytes

class panda_arg_list:
    nargs: int
    list: 'panda_arg'
    plugin_name: bytes

class panda_cb:
    before_block_exec_invalidate_opt: Callable[['CPUState', 'TranslationBlock'], bool]
    before_tcg_codegen: Callable[['CPUState', 'TranslationBlock'], None]
    before_block_exec: Callable[['CPUState', 'TranslationBlock'], None]
    after_block_exec: Callable[['CPUState', 'TranslationBlock', int], None]
    before_block_translate: Callable[['CPUState', int], None]
    after_block_translate: Callable[['CPUState', 'TranslationBlock'], None]
    after_cpu_exec_enter: Callable[['CPUState'], None]
    before_cpu_exec_exit: Callable[['CPUState', bool], None]
    insn_translate: Callable[['CPUState', int], bool]
    insn_exec: Callable[['CPUState', int], int]
    after_insn_translate: Callable[['CPUState', int], bool]
    after_insn_exec: Callable[['CPUState', int], int]
    virt_mem_before_read: Callable[['CPUState', int, int, int], None]
    virt_mem_before_write: Callable[['CPUState', int, int, int, int], None]
    phys_mem_before_read: Callable[['CPUState', int, int, int], None]
    phys_mem_before_write: Callable[['CPUState', int, int, int, int], None]
    virt_mem_after_read: Callable[['CPUState', int, int, int, int], None]
    virt_mem_after_write: Callable[['CPUState', int, int, int, int], None]
    phys_mem_after_read: Callable[['CPUState', int, int, int, int], None]
    phys_mem_after_write: Callable[['CPUState', int, int, int, int], None]
    mmio_after_read: Callable[['CPUState', int, int, int, int], None]
    mmio_before_write: Callable[['CPUState', int, int, int, int], None]
    hd_read: Callable[['CPUState'], None]
    hd_write: Callable[['CPUState'], None]
    guest_hypercall: Callable[['CPUState'], bool]
    monitor: Callable[['Monitor', bytes], int]
    qmp: Callable[[bytes, bytes, bytes], bool]
    cpu_restore_state: Callable[['CPUState', 'TranslationBlock'], None]
    before_loadvm: Callable[[], int]
    asid_changed: Callable[['CPUState', int, int], bool]
    replay_hd_transfer: Callable[['CPUState', int, int, int, int], None]
    replay_before_dma: Callable[['CPUState', int, int, int, bool], None]
    replay_after_dma: Callable[['CPUState', int, int, int, bool], None]
    replay_handle_packet: Callable[['CPUState', int, int, int, int], None]
    replay_net_transfer: Callable[['CPUState', int, int, int, int], None]
    replay_serial_receive: Callable[['CPUState', int, int], None]
    replay_serial_read: Callable[['CPUState', int, int, int], None]
    replay_serial_send: Callable[['CPUState', int, int], None]
    replay_serial_write: Callable[['CPUState', int, int, int], None]
    after_machine_init: Callable[['CPUState'], None]
    after_loadvm: Callable[['CPUState'], None]
    top_loop: Callable[['CPUState'], None]
    during_machine_init: Callable[['MachineState'], None]
    main_loop_wait: Callable[[], None]
    pre_shutdown: Callable[[], None]
    unassigned_io_read: Callable[['CPUState', int, int, int, int], bool]
    unassigned_io_write: Callable[['CPUState', int, int, int, int], bool]
    before_handle_exception: Callable[['CPUState', int], int]
    before_handle_interrupt: Callable[['CPUState', int], int]
    start_block_exec: Callable[['CPUState', 'TranslationBlock'], None]
    end_block_exec: Callable[['CPUState', 'TranslationBlock'], None]
    cbaddr: Callable[[], None]

class panda_cb_list:
    entry: 'panda_cb_with_context'
    owner: ctypes.c_void_p
    next: '_panda_cb_list'
    prev: '_panda_cb_list'
    enabled: bool
    context: ctypes.c_void_p

class panda_cb_type(IntEnum):
    PANDA_CB_LAST = 51
    PANDA_CB_END_BLOCK_EXEC = 50
    PANDA_CB_START_BLOCK_EXEC = 49
    PANDA_CB_BEFORE_HANDLE_INTERRUPT = 48
    PANDA_CB_BEFORE_HANDLE_EXCEPTION = 47
    PANDA_CB_UNASSIGNED_IO_WRITE = 46
    PANDA_CB_UNASSIGNED_IO_READ = 45
    PANDA_CB_PRE_SHUTDOWN = 44
    PANDA_CB_MAIN_LOOP_WAIT = 43
    PANDA_CB_DURING_MACHINE_INIT = 42
    PANDA_CB_TOP_LOOP = 41
    PANDA_CB_AFTER_LOADVM = 40
    PANDA_CB_AFTER_MACHINE_INIT = 39
    PANDA_CB_BEFORE_CPU_EXEC_EXIT = 38
    PANDA_CB_AFTER_CPU_EXEC_ENTER = 37
    PANDA_CB_REPLAY_HANDLE_PACKET = 36
    PANDA_CB_REPLAY_AFTER_DMA = 35
    PANDA_CB_REPLAY_BEFORE_DMA = 34
    PANDA_CB_REPLAY_SERIAL_WRITE = 33
    PANDA_CB_REPLAY_SERIAL_SEND = 32
    PANDA_CB_REPLAY_SERIAL_READ = 31
    PANDA_CB_REPLAY_SERIAL_RECEIVE = 30
    PANDA_CB_REPLAY_NET_TRANSFER = 29
    PANDA_CB_REPLAY_HD_TRANSFER = 28
    PANDA_CB_ASID_CHANGED = 27
    PANDA_CB_BEFORE_LOADVM = 26
    PANDA_CB_CPU_RESTORE_STATE = 25
    PANDA_CB_QMP = 24
    PANDA_CB_MONITOR = 23
    PANDA_CB_GUEST_HYPERCALL = 22
    PANDA_CB_HD_WRITE = 21
    PANDA_CB_HD_READ = 20
    PANDA_CB_MMIO_BEFORE_WRITE = 19
    PANDA_CB_MMIO_AFTER_READ = 18
    PANDA_CB_PHYS_MEM_AFTER_WRITE = 17
    PANDA_CB_PHYS_MEM_AFTER_READ = 16
    PANDA_CB_VIRT_MEM_AFTER_WRITE = 15
    PANDA_CB_VIRT_MEM_AFTER_READ = 14
    PANDA_CB_PHYS_MEM_BEFORE_WRITE = 13
    PANDA_CB_PHYS_MEM_BEFORE_READ = 12
    PANDA_CB_VIRT_MEM_BEFORE_WRITE = 11
    PANDA_CB_VIRT_MEM_BEFORE_READ = 10
    PANDA_CB_AFTER_INSN_EXEC = 9
    PANDA_CB_AFTER_INSN_TRANSLATE = 8
    PANDA_CB_INSN_EXEC = 7
    PANDA_CB_INSN_TRANSLATE = 6
    PANDA_CB_AFTER_BLOCK_EXEC = 5
    PANDA_CB_BEFORE_BLOCK_EXEC = 4
    PANDA_CB_BEFORE_TCG_CODEGEN = 3
    PANDA_CB_BEFORE_BLOCK_EXEC_INVALIDATE_OPT = 2
    PANDA_CB_AFTER_BLOCK_TRANSLATE = 1
    PANDA_CB_BEFORE_BLOCK_TRANSLATE = 0

class panda_cb_with_context:
    before_block_exec_invalidate_opt: Callable[[ctypes.c_void_p, 'CPUState', 'TranslationBlock'], bool]
    before_tcg_codegen: Callable[[ctypes.c_void_p, 'CPUState', 'TranslationBlock'], None]
    before_block_exec: Callable[[ctypes.c_void_p, 'CPUState', 'TranslationBlock'], None]
    after_block_exec: Callable[[ctypes.c_void_p, 'CPUState', 'TranslationBlock', int], None]
    before_block_translate: Callable[[ctypes.c_void_p, 'CPUState', int], None]
    after_block_translate: Callable[[ctypes.c_void_p, 'CPUState', 'TranslationBlock'], None]
    after_cpu_exec_enter: Callable[[ctypes.c_void_p, 'CPUState'], None]
    before_cpu_exec_exit: Callable[[ctypes.c_void_p, 'CPUState', bool], None]
    insn_translate: Callable[[ctypes.c_void_p, 'CPUState', int], bool]
    insn_exec: Callable[[ctypes.c_void_p, 'CPUState', int], int]
    after_insn_translate: Callable[[ctypes.c_void_p, 'CPUState', int], bool]
    after_insn_exec: Callable[[ctypes.c_void_p, 'CPUState', int], int]
    virt_mem_before_read: Callable[[ctypes.c_void_p, 'CPUState', int, int, int], None]
    virt_mem_before_write: Callable[[ctypes.c_void_p, 'CPUState', int, int, int, int], None]
    phys_mem_before_read: Callable[[ctypes.c_void_p, 'CPUState', int, int, int], None]
    phys_mem_before_write: Callable[[ctypes.c_void_p, 'CPUState', int, int, int, int], None]
    virt_mem_after_read: Callable[[ctypes.c_void_p, 'CPUState', int, int, int, int], None]
    virt_mem_after_write: Callable[[ctypes.c_void_p, 'CPUState', int, int, int, int], None]
    phys_mem_after_read: Callable[[ctypes.c_void_p, 'CPUState', int, int, int, int], None]
    phys_mem_after_write: Callable[[ctypes.c_void_p, 'CPUState', int, int, int, int], None]
    mmio_after_read: Callable[[ctypes.c_void_p, 'CPUState', int, int, int, int], None]
    mmio_before_write: Callable[[ctypes.c_void_p, 'CPUState', int, int, int, int], None]
    hd_read: Callable[[ctypes.c_void_p, 'CPUState'], None]
    hd_write: Callable[[ctypes.c_void_p, 'CPUState'], None]
    guest_hypercall: Callable[[ctypes.c_void_p, 'CPUState'], bool]
    monitor: Callable[[ctypes.c_void_p, 'Monitor', bytes], int]
    qmp: Callable[[ctypes.c_void_p, bytes, bytes, bytes], bool]
    cpu_restore_state: Callable[[ctypes.c_void_p, 'CPUState', 'TranslationBlock'], None]
    before_loadvm: Callable[[ctypes.c_void_p], int]
    asid_changed: Callable[[ctypes.c_void_p, 'CPUState', int, int], bool]
    replay_hd_transfer: Callable[[ctypes.c_void_p, 'CPUState', int, int, int, int], None]
    replay_before_dma: Callable[[ctypes.c_void_p, 'CPUState', int, int, int, bool], None]
    replay_after_dma: Callable[[ctypes.c_void_p, 'CPUState', int, int, int, bool], None]
    replay_handle_packet: Callable[[ctypes.c_void_p, 'CPUState', int, int, int, int], None]
    replay_net_transfer: Callable[[ctypes.c_void_p, 'CPUState', int, int, int, int], None]
    replay_serial_receive: Callable[[ctypes.c_void_p, 'CPUState', int, int], None]
    replay_serial_read: Callable[[ctypes.c_void_p, 'CPUState', int, int, int], None]
    replay_serial_send: Callable[[ctypes.c_void_p, 'CPUState', int, int], None]
    replay_serial_write: Callable[[ctypes.c_void_p, 'CPUState', int, int, int], None]
    after_machine_init: Callable[[ctypes.c_void_p, 'CPUState'], None]
    after_loadvm: Callable[[ctypes.c_void_p, 'CPUState'], None]
    top_loop: Callable[[ctypes.c_void_p, 'CPUState'], None]
    during_machine_init: Callable[[ctypes.c_void_p, 'MachineState'], None]
    main_loop_wait: Callable[[ctypes.c_void_p], None]
    pre_shutdown: Callable[[ctypes.c_void_p], None]
    unassigned_io_read: Callable[[ctypes.c_void_p, 'CPUState', int, int, int, int], bool]
    unassigned_io_write: Callable[[ctypes.c_void_p, 'CPUState', int, int, int, int], bool]
    before_handle_exception: Callable[[ctypes.c_void_p, 'CPUState', int], int]
    before_handle_interrupt: Callable[[ctypes.c_void_p, 'CPUState', int], int]
    start_block_exec: Callable[[ctypes.c_void_p, 'CPUState', 'TranslationBlock'], None]
    end_block_exec: Callable[[ctypes.c_void_p, 'CPUState', 'TranslationBlock'], None]
    cbaddr: Callable[[], None]

class panda_plugin:
    name: bytes
    plugin: ctypes.c_void_p
    unload: bool
    exported_symbols: bool

powerpc_excp_t: int
powerpc_input_t: int
powerpc_mmu_t: int
ppc_avr_t: list[int]
ppc_tlb_t: list[int]
pthread_cond_t: list[int]
pthread_mutex_t: list[int]
pthread_t: int
class qemu_work_item:
    next: 'qemu_work_item'
    func: ctypes.c_void_p
    data: int
    free: bool
    exclusive: bool
    done: bool

ram_addr_t: int
class rcu_head:
    next: 'rcu_head'
    func: Callable[['rcu_head'], None]

run_on_cpu_data: int
run_on_cpu_func: ctypes.c_void_p
sigjmp_buf: list[int]
class subregions:
    tqh_first: 'MemoryRegion'
    tqh_last: 'MemoryRegion'

class syscall_argtype_t(IntEnum):
    SYSCALL_ARG_ARR = 49
    SYSCALL_ARG_STRUCT = 48
    SYSCALL_ARG_STR_PTR = 34
    SYSCALL_ARG_STRUCT_PTR = 33
    SYSCALL_ARG_BUF_PTR = 32
    SYSCALL_ARG_S16 = 18
    SYSCALL_ARG_S32 = 17
    SYSCALL_ARG_S64 = 16
    SYSCALL_ARG_U16 = 2
    SYSCALL_ARG_U32 = 1
    SYSCALL_ARG_U64 = 0

class syscall_ctx_t:
    no: int
    asid: int
    retaddr: int
    args: list[list[int]]

class syscall_info_t:
    no: int
    name: bytes
    nargs: int
    argt: 'syscall_argtype_t'
    argsz: int
    argn: bytes
    argtn: bytes
    noreturn: bool

class syscall_meta_t:
    max: int
    max_generic: int
    max_args: int

target_long: int
target_pid_t: int
target_ptr_t: int
target_ulong: int
tb_page_addr_t: int
vaddr: int
class watchpoints_head:
    tqh_first: 'CPUWatchpoint'
    tqh_last: 'CPUWatchpoint'

class AddressSpaceDispatch:
    pass

class BusChild:
    pass

class CoalescedMemoryRange:
    pass

class FlatView:
    pass

class IOMMUNotifier:
    pass

class KVMState:
    pass

class NamedGPIOList:
    pass

class QemuOpt:
    pass

class RAMBlockNotifier:
    pass

class _IO_FILE:
    pass

class _panda_cb_list:
    entry: 'panda_cb_with_context'
    owner: ctypes.c_void_p
    next: '_panda_cb_list'
    prev: '_panda_cb_list'
    enabled: bool
    context: ctypes.c_void_p

class addr_struct:
    typ: 'AddrType'
    val: int
    off: int
    flag: 'AddrFlag'

class arm_boot_info:
    pass

class auxv_values:
    argc: int
    argv_ptr_ptr: int
    arg_ptr: list[int]
    argv: list[list[bytes]]
    envc: int
    env_ptr_ptr: int
    env_ptr: list[int]
    envp: list[list[bytes]]
    execfn_ptr: int
    execfn: list[bytes]
    phdr: int
    entry: int
    ehdr: int
    hwcap: int
    hwcap2: int
    pagesz: int
    clktck: int
    phent: int
    phnum: int
    base: int
    flags: int
    uid: int
    euid: int
    gid: int
    egid: int
    secure: bool
    random: int
    platform: int
    program_header: int
    minsigstksz: int

class cred_info:
    uid_offset: int
    gid_offset: int
    euid_offset: int
    egid_offset: int

class dynamic_symbol_hook:
    library_name: list[bytes]
    symbol: list[bytes]
    cb: Callable[['CPUState', 'TranslationBlock', 'hook'], bool]

class fs_info:
    f_path_dentry_offset: int
    f_dentry_offset: int
    f_path_mnt_offset: int
    f_vfsmnt_offset: int
    f_pos_offset: int
    fdt_offset: int
    fdtab_offset: int
    fd_offset: int

class hax_state:
    pass

class hax_tunnel:
    pass

class hook_symbol_resolve:
    name: list[bytes]
    offset: int
    hook_offset: bool
    section: list[bytes]
    cb: Callable[['hook_symbol_resolve', 'symbol', int], None]
    enabled: bool
    id: int

class kernelinfo:
    name: bytes
    version: 'version'
    task: 'task_info'
    cred: 'cred_info'
    mm: 'mm_info'
    vma: 'vma_info'
    fs: 'fs_info'
    qstr: 'qstr_info'
    path: 'path_info'

class kvm_run:
    pass

class memory_access_desc:
    pc: int
    addr: int
    size: int
    buf: int
    on_before: bool
    on_after: bool
    on_read: bool
    on_write: bool
    on_virtual: bool
    on_physical: bool
    hook: 'memory_hooks_region'

class memory_hooks_region:
    start_address: int
    stop_address: int
    enabled: bool
    on_before: bool
    on_after: bool
    on_read: bool
    on_write: bool
    on_virtual: bool
    on_physical: bool
    cb: Callable[['CPUState', 'memory_access_desc'], None]

class mm_info:
    size: int
    mmap_offset: int
    pgd_offset: int
    arg_start_offset: int
    start_brk_offset: int
    brk_offset: int
    start_stack_offset: int

class mon_fd_t:
    pass

class osi_module_struct:
    modd: int
    base: int
    size: int
    file: bytes
    name: bytes
    offset: int
    flags: int

class osi_page_struct:
    start: int
    len: int

class osi_proc_handle_struct:
    taskd: int
    asid: int

class osi_proc_mem:
    start_brk: int
    brk: int

class osi_proc_struct:
    taskd: int
    pgd: int
    asid: int
    pid: int
    ppid: int
    name: bytes
    pages: 'osi_page_struct'
    create_time: int

class osi_thread_struct:
    pid: int
    tid: int

class path_info:
    d_name_offset: int
    d_iname_offset: int
    d_parent_offset: int
    d_op_offset: int
    d_dname_offset: int
    mnt_root_offset: int
    mnt_parent_offset: int
    mnt_mountpoint_offset: int

class qstr_info:
    size: int
    name_offset: int

class query_result:
    num_labels: int
    ls: ctypes.c_void_p
    it_end: ctypes.c_void_p
    it_curr: ctypes.c_void_p
    tcn: int
    cb_mask: int

class symbol:
    address: int
    value: int
    symtab_idx: int
    reloc_type: int
    name: list[bytes]
    section: list[bytes]

class symbol_hook:
    name: list[bytes]
    offset: int
    hook_offset: bool
    section: list[bytes]
    type: 'panda_cb_type'
    cb: 'hooks_panda_cb'

class syscall_ctx:
    no: int
    asid: int
    retaddr: int
    args: list[list[int]]

class task_info:
    per_cpu_offsets_addr: int
    per_cpu_offset_0_addr: int
    switch_task_hook_addr: int
    current_task_addr: int
    init_addr: int
    size: int
    tasks_offset: int
    next_task_offset: int
    pid_offset: int
    tgid_offset: int
    group_leader_offset: int
    thread_group_offset: int
    real_parent_offset: int
    p_opptr_offset: int
    parent_offset: int
    p_pptr_offset: int
    mm_offset: int
    stack_offset: int
    real_cred_offset: int
    cred_offset: int
    comm_offset: int
    comm_size: int
    files_offset: int
    start_time_offset: int

class version:
    a: int
    b: int
    c: int

class vma_info:
    size: int
    vm_mm_offset: int
    vm_start_offset: int
    vm_end_offset: int
    vm_next_offset: int
    vm_file_offset: int
    vm_flags_offset: int

class device_endian(IntEnum):
    DEVICE_LITTLE_ENDIAN = 2
    DEVICE_BIG_ENDIAN = 1
    DEVICE_NATIVE_ENDIAN = 0

class QemuOptType(IntEnum):
    QEMU_OPT_SIZE = 3
    QEMU_OPT_NUMBER = 2
    QEMU_OPT_BOOL = 1
    QEMU_OPT_STRING = 0

class kernel_mode(IntEnum):
    MODE_USER_ONLY = 2
    MODE_KERNEL_ONLY = 1
    MODE_ANY = 0

