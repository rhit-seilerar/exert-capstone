from enum import IntEnum
from collections.abc import Callable
import ctypes
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

class BNDCSReg:
    cfgu: int
    sts: int

class BNDReg:
    lb: int
    ub: int

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
    env_ptr: 'CPUX86State'
    tb_jmp_cache: list['TranslationBlock']
    gdb_regs: 'GDBRegisterState'
    gdb_num_regs: int
    gdb_num_g_regs: int
    class internal_23:
        tqe_next: 'CPUState'
        tqe_prev: 'CPUState'

    node: internal_23
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
    class internal_24:
        u32: int
        u16: 'icount_decr_u16'

    icount_decr: internal_24
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
class CPUX86State:
    regs: list[int]
    eip: int
    eflags: int
    cc_dst: int
    cc_src: int
    cc_src2: int
    cc_op: int
    df: int
    hflags: int
    hflags2: int
    segs: list['SegmentCache']
    ldt: 'SegmentCache'
    tr: 'SegmentCache'
    gdt: 'SegmentCache'
    idt: 'SegmentCache'
    cr: list[int]
    a20_mask: int
    bnd_regs: list['BNDReg']
    bndcs_regs: 'BNDCSReg'
    msr_bndcfgs: int
    efer: int
    fpstt: int
    fpus: int
    fpuc: int
    fptags: list[int]
    fpregs: list[list[int]]
    fpop: int
    fpip: int
    fpdp: int
    fp_status: 'float_status'
    ft0: 'floatx80'
    mmx_status: 'float_status'
    sse_status: 'float_status'
    mxcsr: int
    xmm_regs: list[list[int]]
    xmm_t0: list[int]
    mmx_t0: list[int]
    opmask_regs: list[int]
    sysenter_cs: int
    sysenter_esp: int
    sysenter_eip: int
    star: int
    vm_hsave: int
    lstar: int
    cstar: int
    fmask: int
    kernelgsbase: int
    tsc: int
    tsc_adjust: int
    tsc_deadline: int
    tsc_aux: int
    xcr0: int
    mcg_status: int
    msr_ia32_misc_enable: int
    msr_ia32_feature_control: int
    msr_fixed_ctr_ctrl: int
    msr_global_ctrl: int
    msr_global_status: int
    msr_global_ovf_ctrl: int
    msr_fixed_counters: list[int]
    msr_gp_counters: list[int]
    msr_gp_evtsel: list[int]
    pat: int
    smbase: int
    pkru: int
    system_time_msr: int
    wall_clock_msr: int
    steal_time_msr: int
    async_pf_en_msr: int
    pv_eoi_en_msr: int
    msr_hv_hypercall: int
    msr_hv_guest_os_id: int
    msr_hv_vapic: int
    msr_hv_tsc: int
    msr_hv_crash_params: list[int]
    msr_hv_runtime: int
    msr_hv_synic_control: int
    msr_hv_synic_version: int
    msr_hv_synic_evt_page: int
    msr_hv_synic_msg_page: int
    msr_hv_synic_sint: list[int]
    msr_hv_stimer_config: list[int]
    msr_hv_stimer_count: list[int]
    error_code: int
    exception_is_int: int
    exception_next_eip: int
    dr: list[int]
    cpu_breakpoint: list['CPUBreakpoint']
    cpu_watchpoint: list['CPUWatchpoint']
    old_exception: int
    vm_vmcb: int
    tsc_offset: int
    intercept: int
    intercept_cr_read: int
    intercept_cr_write: int
    intercept_dr_read: int
    intercept_dr_write: int
    intercept_exceptions: int
    v_tpr: int
    nmi_injected: int
    nmi_pending: int
    tlb_table: list[list['CPUTLBEntry']]
    tlb_v_table: list[list['CPUTLBEntry']]
    iotlb: list[list['CPUIOTLBEntry']]
    iotlb_v: list[list['CPUIOTLBEntry']]
    tlb_flush_addr: int
    tlb_flush_mask: int
    vtlb_index: int
    cpuid_min_level: int
    cpuid_min_xlevel: int
    cpuid_min_xlevel2: int
    cpuid_max_level: int
    cpuid_max_xlevel: int
    cpuid_max_xlevel2: int
    cpuid_level: int
    cpuid_xlevel: int
    cpuid_xlevel2: int
    cpuid_vendor1: int
    cpuid_vendor2: int
    cpuid_vendor3: int
    cpuid_version: int
    features: list[int]
    user_features: list[int]
    cpuid_model: list[int]
    mtrr_fixed: list[int]
    mtrr_deftype: int
    mtrr_var: list['MTRRVar']
    mp_state: int
    exception_injected: int
    interrupt_injected: int
    soft_interrupt: int
    has_error_code: int
    sipi_vector: int
    tsc_valid: bool
    tsc_khz: int
    user_tsc_khz: int
    kvm_xsave_buf: ctypes.c_void_p
    mcg_cap: int
    mcg_ctl: int
    mcg_ext_ctl: int
    mce_banks: list[int]
    xstate_bv: int
    fpus_vmstate: int
    fptag_vmstate: int
    fpregs_format_vmstate: int
    xss: int
    tpr_access_type: 'TPRAccess'

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
class SegmentCache:
    selector: int
    base: int
    limit: int
    flags: int

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
on_NtAcceptConnectPort_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAcceptConnectPort_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAccessCheckAndAuditAlarm_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtAccessCheckAndAuditAlarm_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtAccessCheckByTypeAndAuditAlarm_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtAccessCheckByTypeAndAuditAlarm_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtAccessCheckByTypeResultListAndAuditAlarmByHandle_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtAccessCheckByTypeResultListAndAuditAlarmByHandle_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtAccessCheckByTypeResultListAndAuditAlarm_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtAccessCheckByTypeResultListAndAuditAlarm_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtAccessCheckByTypeResultList_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtAccessCheckByTypeResultList_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtAccessCheckByType_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtAccessCheckByType_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtAccessCheck_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtAccessCheck_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtAddAtom_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtAddAtom_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtAddBootEntry_enter_t: Callable[['CPUState', int, int, int], None]
on_NtAddBootEntry_return_t: Callable[['CPUState', int, int, int], None]
on_NtAddDriverEntry_enter_t: Callable[['CPUState', int, int, int], None]
on_NtAddDriverEntry_return_t: Callable[['CPUState', int, int, int], None]
on_NtAdjustGroupsToken_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAdjustGroupsToken_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAdjustPrivilegesToken_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAdjustPrivilegesToken_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAlertResumeThread_enter_t: Callable[['CPUState', int, int, int], None]
on_NtAlertResumeThread_return_t: Callable[['CPUState', int, int, int], None]
on_NtAlertThread_enter_t: Callable[['CPUState', int, int], None]
on_NtAlertThread_return_t: Callable[['CPUState', int, int], None]
on_NtAllocateLocallyUniqueId_enter_t: Callable[['CPUState', int, int], None]
on_NtAllocateLocallyUniqueId_return_t: Callable[['CPUState', int, int], None]
on_NtAllocateReserveObject_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtAllocateReserveObject_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtAllocateUserPhysicalPages_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtAllocateUserPhysicalPages_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtAllocateUuids_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtAllocateUuids_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtAllocateVirtualMemory_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAllocateVirtualMemory_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAlpcAcceptConnectPort_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtAlpcAcceptConnectPort_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtAlpcCancelMessage_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcCancelMessage_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcConnectPort_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtAlpcConnectPort_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtAlpcCreatePortSection_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAlpcCreatePortSection_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAlpcCreatePort_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcCreatePort_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcCreateResourceReserve_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtAlpcCreateResourceReserve_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtAlpcCreateSectionView_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcCreateSectionView_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcCreateSecurityContext_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcCreateSecurityContext_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcDeletePortSection_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcDeletePortSection_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcDeleteResourceReserve_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcDeleteResourceReserve_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcDeleteSectionView_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcDeleteSectionView_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcDeleteSecurityContext_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcDeleteSecurityContext_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcDisconnectPort_enter_t: Callable[['CPUState', int, int, int], None]
on_NtAlpcDisconnectPort_return_t: Callable[['CPUState', int, int, int], None]
on_NtAlpcImpersonateClientOfPort_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcImpersonateClientOfPort_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcOpenSenderProcess_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAlpcOpenSenderProcess_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAlpcOpenSenderThread_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAlpcOpenSenderThread_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAlpcQueryInformationMessage_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAlpcQueryInformationMessage_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtAlpcQueryInformation_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtAlpcQueryInformation_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtAlpcRevokeSecurityContext_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcRevokeSecurityContext_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtAlpcSendWaitReceivePort_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtAlpcSendWaitReceivePort_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtAlpcSetInformation_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtAlpcSetInformation_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtApphelpCacheControl_enter_t: Callable[['CPUState', int, int, int], None]
on_NtApphelpCacheControl_return_t: Callable[['CPUState', int, int, int], None]
on_NtAreMappedFilesTheSame_enter_t: Callable[['CPUState', int, int, int], None]
on_NtAreMappedFilesTheSame_return_t: Callable[['CPUState', int, int, int], None]
on_NtAssignProcessToJobObject_enter_t: Callable[['CPUState', int, int, int], None]
on_NtAssignProcessToJobObject_return_t: Callable[['CPUState', int, int, int], None]
on_NtCallbackReturn_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtCallbackReturn_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtCancelIoFileEx_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtCancelIoFileEx_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtCancelIoFile_enter_t: Callable[['CPUState', int, int, int], None]
on_NtCancelIoFile_return_t: Callable[['CPUState', int, int, int], None]
on_NtCancelSynchronousIoFile_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtCancelSynchronousIoFile_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtCancelTimer_enter_t: Callable[['CPUState', int, int, int], None]
on_NtCancelTimer_return_t: Callable[['CPUState', int, int, int], None]
on_NtClearEvent_enter_t: Callable[['CPUState', int, int], None]
on_NtClearEvent_return_t: Callable[['CPUState', int, int], None]
on_NtCloseObjectAuditAlarm_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtCloseObjectAuditAlarm_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtClose_enter_t: Callable[['CPUState', int, int], None]
on_NtClose_return_t: Callable[['CPUState', int, int], None]
on_NtCommitComplete_enter_t: Callable[['CPUState', int, int, int], None]
on_NtCommitComplete_return_t: Callable[['CPUState', int, int, int], None]
on_NtCommitEnlistment_enter_t: Callable[['CPUState', int, int, int], None]
on_NtCommitEnlistment_return_t: Callable[['CPUState', int, int, int], None]
on_NtCommitTransaction_enter_t: Callable[['CPUState', int, int, int], None]
on_NtCommitTransaction_return_t: Callable[['CPUState', int, int, int], None]
on_NtCompactKeys_enter_t: Callable[['CPUState', int, int, int], None]
on_NtCompactKeys_return_t: Callable[['CPUState', int, int, int], None]
on_NtCompareTokens_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtCompareTokens_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtCompleteConnectPort_enter_t: Callable[['CPUState', int, int], None]
on_NtCompleteConnectPort_return_t: Callable[['CPUState', int, int], None]
on_NtCompressKey_enter_t: Callable[['CPUState', int, int], None]
on_NtCompressKey_return_t: Callable[['CPUState', int, int], None]
on_NtConnectPort_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtConnectPort_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtContinue_enter_t: Callable[['CPUState', int, int, int], None]
on_NtContinue_return_t: Callable[['CPUState', int, int, int], None]
on_NtCreateDebugObject_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreateDebugObject_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreateDirectoryObject_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtCreateDirectoryObject_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtCreateEnlistment_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtCreateEnlistment_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtCreateEventPair_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtCreateEventPair_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtCreateEvent_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtCreateEvent_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtCreateFile_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateFile_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateIoCompletion_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreateIoCompletion_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreateJobObject_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtCreateJobObject_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtCreateJobSet_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtCreateJobSet_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtCreateKeyTransacted_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtCreateKeyTransacted_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtCreateKey_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtCreateKey_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtCreateKeyedEvent_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreateKeyedEvent_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreateMailslotFile_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtCreateMailslotFile_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtCreateMutant_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreateMutant_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreateNamedPipeFile_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateNamedPipeFile_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtCreatePagingFile_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreatePagingFile_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreatePort_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtCreatePort_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtCreatePrivateNamespace_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreatePrivateNamespace_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreateProcessEx_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateProcessEx_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateProcess_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtCreateProcess_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtCreateProfileEx_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateProfileEx_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateProfile_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateProfile_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateResourceManager_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtCreateResourceManager_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtCreateSection_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtCreateSection_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtCreateSemaphore_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtCreateSemaphore_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtCreateSymbolicLinkObject_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreateSymbolicLinkObject_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreateThreadEx_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateThreadEx_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateThread_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtCreateThread_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtCreateTimer_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreateTimer_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtCreateToken_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateToken_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateTransactionManager_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtCreateTransactionManager_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtCreateTransaction_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateTransaction_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateUserProcess_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateUserProcess_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateWaitablePort_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtCreateWaitablePort_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtCreateWorkerFactory_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtCreateWorkerFactory_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtDebugActiveProcess_enter_t: Callable[['CPUState', int, int, int], None]
on_NtDebugActiveProcess_return_t: Callable[['CPUState', int, int, int], None]
on_NtDebugContinue_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtDebugContinue_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtDelayExecution_enter_t: Callable[['CPUState', int, int, int], None]
on_NtDelayExecution_return_t: Callable[['CPUState', int, int, int], None]
on_NtDeleteAtom_enter_t: Callable[['CPUState', int, int], None]
on_NtDeleteAtom_return_t: Callable[['CPUState', int, int], None]
on_NtDeleteBootEntry_enter_t: Callable[['CPUState', int, int], None]
on_NtDeleteBootEntry_return_t: Callable[['CPUState', int, int], None]
on_NtDeleteDriverEntry_enter_t: Callable[['CPUState', int, int], None]
on_NtDeleteDriverEntry_return_t: Callable[['CPUState', int, int], None]
on_NtDeleteFile_enter_t: Callable[['CPUState', int, int], None]
on_NtDeleteFile_return_t: Callable[['CPUState', int, int], None]
on_NtDeleteKey_enter_t: Callable[['CPUState', int, int], None]
on_NtDeleteKey_return_t: Callable[['CPUState', int, int], None]
on_NtDeleteObjectAuditAlarm_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtDeleteObjectAuditAlarm_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtDeletePrivateNamespace_enter_t: Callable[['CPUState', int, int], None]
on_NtDeletePrivateNamespace_return_t: Callable[['CPUState', int, int], None]
on_NtDeleteValueKey_enter_t: Callable[['CPUState', int, int, int], None]
on_NtDeleteValueKey_return_t: Callable[['CPUState', int, int, int], None]
on_NtDeviceIoControlFile_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtDeviceIoControlFile_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtDisableLastKnownGood_enter_t: Callable[['CPUState', int], None]
on_NtDisableLastKnownGood_return_t: Callable[['CPUState', int], None]
on_NtDisplayString_enter_t: Callable[['CPUState', int, int], None]
on_NtDisplayString_return_t: Callable[['CPUState', int, int], None]
on_NtDrawText_enter_t: Callable[['CPUState', int, int], None]
on_NtDrawText_return_t: Callable[['CPUState', int, int], None]
on_NtDuplicateObject_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtDuplicateObject_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtDuplicateToken_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtDuplicateToken_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtEnableLastKnownGood_enter_t: Callable[['CPUState', int], None]
on_NtEnableLastKnownGood_return_t: Callable[['CPUState', int], None]
on_NtEnumerateBootEntries_enter_t: Callable[['CPUState', int, int, int], None]
on_NtEnumerateBootEntries_return_t: Callable[['CPUState', int, int, int], None]
on_NtEnumerateDriverEntries_enter_t: Callable[['CPUState', int, int, int], None]
on_NtEnumerateDriverEntries_return_t: Callable[['CPUState', int, int, int], None]
on_NtEnumerateKey_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtEnumerateKey_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtEnumerateSystemEnvironmentValuesEx_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtEnumerateSystemEnvironmentValuesEx_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtEnumerateTransactionObject_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtEnumerateTransactionObject_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtEnumerateValueKey_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtEnumerateValueKey_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtExtendSection_enter_t: Callable[['CPUState', int, int, int], None]
on_NtExtendSection_return_t: Callable[['CPUState', int, int, int], None]
on_NtFilterToken_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtFilterToken_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtFindAtom_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtFindAtom_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtFlushBuffersFile_enter_t: Callable[['CPUState', int, int, int], None]
on_NtFlushBuffersFile_return_t: Callable[['CPUState', int, int, int], None]
on_NtFlushInstallUILanguage_enter_t: Callable[['CPUState', int, int, int], None]
on_NtFlushInstallUILanguage_return_t: Callable[['CPUState', int, int, int], None]
on_NtFlushInstructionCache_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtFlushInstructionCache_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtFlushKey_enter_t: Callable[['CPUState', int, int], None]
on_NtFlushKey_return_t: Callable[['CPUState', int, int], None]
on_NtFlushProcessWriteBuffers_enter_t: Callable[['CPUState', int], None]
on_NtFlushProcessWriteBuffers_return_t: Callable[['CPUState', int], None]
on_NtFlushVirtualMemory_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtFlushVirtualMemory_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtFlushWriteBuffer_enter_t: Callable[['CPUState', int], None]
on_NtFlushWriteBuffer_return_t: Callable[['CPUState', int], None]
on_NtFreeUserPhysicalPages_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtFreeUserPhysicalPages_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtFreeVirtualMemory_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtFreeVirtualMemory_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtFreezeRegistry_enter_t: Callable[['CPUState', int, int], None]
on_NtFreezeRegistry_return_t: Callable[['CPUState', int, int], None]
on_NtFreezeTransactions_enter_t: Callable[['CPUState', int, int, int], None]
on_NtFreezeTransactions_return_t: Callable[['CPUState', int, int, int], None]
on_NtFsControlFile_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtFsControlFile_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtGetContextThread_enter_t: Callable[['CPUState', int, int, int], None]
on_NtGetContextThread_return_t: Callable[['CPUState', int, int, int], None]
on_NtGetCurrentProcessorNumber_enter_t: Callable[['CPUState', int], None]
on_NtGetCurrentProcessorNumber_return_t: Callable[['CPUState', int], None]
on_NtGetDevicePowerState_enter_t: Callable[['CPUState', int, int, int], None]
on_NtGetDevicePowerState_return_t: Callable[['CPUState', int, int, int], None]
on_NtGetMUIRegistryInfo_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtGetMUIRegistryInfo_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtGetNextProcess_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtGetNextProcess_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtGetNextThread_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtGetNextThread_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtGetNlsSectionPtr_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtGetNlsSectionPtr_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtGetNotificationResourceManager_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtGetNotificationResourceManager_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtGetPlugPlayEvent_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtGetPlugPlayEvent_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtGetWriteWatch_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtGetWriteWatch_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtImpersonateAnonymousToken_enter_t: Callable[['CPUState', int, int], None]
on_NtImpersonateAnonymousToken_return_t: Callable[['CPUState', int, int], None]
on_NtImpersonateClientOfPort_enter_t: Callable[['CPUState', int, int, int], None]
on_NtImpersonateClientOfPort_return_t: Callable[['CPUState', int, int, int], None]
on_NtImpersonateThread_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtImpersonateThread_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtInitializeNlsFiles_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtInitializeNlsFiles_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtInitializeRegistry_enter_t: Callable[['CPUState', int, int], None]
on_NtInitializeRegistry_return_t: Callable[['CPUState', int, int], None]
on_NtInitiatePowerAction_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtInitiatePowerAction_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtIsProcessInJob_enter_t: Callable[['CPUState', int, int, int], None]
on_NtIsProcessInJob_return_t: Callable[['CPUState', int, int, int], None]
on_NtIsSystemResumeAutomatic_enter_t: Callable[['CPUState', int], None]
on_NtIsSystemResumeAutomatic_return_t: Callable[['CPUState', int], None]
on_NtIsUILanguageComitted_enter_t: Callable[['CPUState', int], None]
on_NtIsUILanguageComitted_return_t: Callable[['CPUState', int], None]
on_NtListenPort_enter_t: Callable[['CPUState', int, int, int], None]
on_NtListenPort_return_t: Callable[['CPUState', int, int, int], None]
on_NtLoadDriver_enter_t: Callable[['CPUState', int, int], None]
on_NtLoadDriver_return_t: Callable[['CPUState', int, int], None]
on_NtLoadKey2_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtLoadKey2_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtLoadKeyEx_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtLoadKeyEx_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtLoadKey_enter_t: Callable[['CPUState', int, int, int], None]
on_NtLoadKey_return_t: Callable[['CPUState', int, int, int], None]
on_NtLockFile_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtLockFile_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtLockProductActivationKeys_enter_t: Callable[['CPUState', int, int, int], None]
on_NtLockProductActivationKeys_return_t: Callable[['CPUState', int, int, int], None]
on_NtLockRegistryKey_enter_t: Callable[['CPUState', int, int], None]
on_NtLockRegistryKey_return_t: Callable[['CPUState', int, int], None]
on_NtLockVirtualMemory_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtLockVirtualMemory_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtMakePermanentObject_enter_t: Callable[['CPUState', int, int], None]
on_NtMakePermanentObject_return_t: Callable[['CPUState', int, int], None]
on_NtMakeTemporaryObject_enter_t: Callable[['CPUState', int, int], None]
on_NtMakeTemporaryObject_return_t: Callable[['CPUState', int, int], None]
on_NtMapCMFModule_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtMapCMFModule_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtMapUserPhysicalPagesScatter_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtMapUserPhysicalPagesScatter_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtMapUserPhysicalPages_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtMapUserPhysicalPages_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtMapViewOfSection_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtMapViewOfSection_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtModifyBootEntry_enter_t: Callable[['CPUState', int, int], None]
on_NtModifyBootEntry_return_t: Callable[['CPUState', int, int], None]
on_NtModifyDriverEntry_enter_t: Callable[['CPUState', int, int], None]
on_NtModifyDriverEntry_return_t: Callable[['CPUState', int, int], None]
on_NtNotifyChangeDirectoryFile_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtNotifyChangeDirectoryFile_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtNotifyChangeKey_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtNotifyChangeKey_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int], None]
on_NtNotifyChangeMultipleKeys_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtNotifyChangeMultipleKeys_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtNotifyChangeSession_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtNotifyChangeSession_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int], None]
on_NtOpenDirectoryObject_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenDirectoryObject_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenEnlistment_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtOpenEnlistment_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtOpenEventPair_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenEventPair_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenEvent_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenEvent_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenFile_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtOpenFile_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtOpenIoCompletion_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenIoCompletion_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenJobObject_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenJobObject_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenKeyEx_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtOpenKeyEx_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtOpenKeyTransactedEx_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtOpenKeyTransactedEx_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtOpenKeyTransacted_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtOpenKeyTransacted_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtOpenKey_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenKey_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenKeyedEvent_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenKeyedEvent_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenMutant_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenMutant_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenObjectAuditAlarm_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtOpenObjectAuditAlarm_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtOpenPrivateNamespace_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtOpenPrivateNamespace_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtOpenProcessTokenEx_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtOpenProcessTokenEx_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtOpenProcessToken_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenProcessToken_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenProcess_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtOpenProcess_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtOpenResourceManager_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtOpenResourceManager_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtOpenSection_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenSection_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenSemaphore_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenSemaphore_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenSession_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenSession_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenSymbolicLinkObject_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenSymbolicLinkObject_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenThreadTokenEx_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtOpenThreadTokenEx_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtOpenThreadToken_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtOpenThreadToken_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtOpenThread_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtOpenThread_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtOpenTimer_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenTimer_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtOpenTransactionManager_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtOpenTransactionManager_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtOpenTransaction_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtOpenTransaction_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtPlugPlayControl_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtPlugPlayControl_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtPowerInformation_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtPowerInformation_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtPrePrepareComplete_enter_t: Callable[['CPUState', int, int, int], None]
on_NtPrePrepareComplete_return_t: Callable[['CPUState', int, int, int], None]
on_NtPrePrepareEnlistment_enter_t: Callable[['CPUState', int, int, int], None]
on_NtPrePrepareEnlistment_return_t: Callable[['CPUState', int, int, int], None]
on_NtPrepareComplete_enter_t: Callable[['CPUState', int, int, int], None]
on_NtPrepareComplete_return_t: Callable[['CPUState', int, int, int], None]
on_NtPrepareEnlistment_enter_t: Callable[['CPUState', int, int, int], None]
on_NtPrepareEnlistment_return_t: Callable[['CPUState', int, int, int], None]
on_NtPrivilegeCheck_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtPrivilegeCheck_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtPrivilegeObjectAuditAlarm_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtPrivilegeObjectAuditAlarm_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtPrivilegedServiceAuditAlarm_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtPrivilegedServiceAuditAlarm_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtPropagationComplete_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtPropagationComplete_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtPropagationFailed_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtPropagationFailed_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtProtectVirtualMemory_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtProtectVirtualMemory_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtPulseEvent_enter_t: Callable[['CPUState', int, int, int], None]
on_NtPulseEvent_return_t: Callable[['CPUState', int, int, int], None]
on_NtQueryAttributesFile_enter_t: Callable[['CPUState', int, int, int], None]
on_NtQueryAttributesFile_return_t: Callable[['CPUState', int, int, int], None]
on_NtQueryBootEntryOrder_enter_t: Callable[['CPUState', int, int, int], None]
on_NtQueryBootEntryOrder_return_t: Callable[['CPUState', int, int, int], None]
on_NtQueryBootOptions_enter_t: Callable[['CPUState', int, int, int], None]
on_NtQueryBootOptions_return_t: Callable[['CPUState', int, int, int], None]
on_NtQueryDebugFilterState_enter_t: Callable[['CPUState', int, int, int], None]
on_NtQueryDebugFilterState_return_t: Callable[['CPUState', int, int, int], None]
on_NtQueryDefaultLocale_enter_t: Callable[['CPUState', int, int, int], None]
on_NtQueryDefaultLocale_return_t: Callable[['CPUState', int, int, int], None]
on_NtQueryDefaultUILanguage_enter_t: Callable[['CPUState', int, int], None]
on_NtQueryDefaultUILanguage_return_t: Callable[['CPUState', int, int], None]
on_NtQueryDirectoryFile_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtQueryDirectoryFile_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int, int, int], None]
on_NtQueryDirectoryObject_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtQueryDirectoryObject_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtQueryDriverEntryOrder_enter_t: Callable[['CPUState', int, int, int], None]
on_NtQueryDriverEntryOrder_return_t: Callable[['CPUState', int, int, int], None]
on_NtQueryEaFile_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtQueryEaFile_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtQueryEvent_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryEvent_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryFullAttributesFile_enter_t: Callable[['CPUState', int, int, int], None]
on_NtQueryFullAttributesFile_return_t: Callable[['CPUState', int, int, int], None]
on_NtQueryInformationAtom_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationAtom_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationEnlistment_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationEnlistment_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationFile_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationFile_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationJobObject_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationJobObject_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationPort_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationPort_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationProcess_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationProcess_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationResourceManager_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationResourceManager_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationThread_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationThread_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationToken_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationToken_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationTransactionManager_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationTransactionManager_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationTransaction_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationTransaction_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationWorkerFactory_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInformationWorkerFactory_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryInstallUILanguage_enter_t: Callable[['CPUState', int, int], None]
on_NtQueryInstallUILanguage_return_t: Callable[['CPUState', int, int], None]
on_NtQueryIntervalProfile_enter_t: Callable[['CPUState', int, int, int], None]
on_NtQueryIntervalProfile_return_t: Callable[['CPUState', int, int, int], None]
on_NtQueryIoCompletion_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryIoCompletion_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryKey_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryKey_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryLicenseValue_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryLicenseValue_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryMultipleValueKey_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtQueryMultipleValueKey_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtQueryMutant_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryMutant_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryObject_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryObject_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryOpenSubKeysEx_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtQueryOpenSubKeysEx_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtQueryOpenSubKeys_enter_t: Callable[['CPUState', int, int, int], None]
on_NtQueryOpenSubKeys_return_t: Callable[['CPUState', int, int, int], None]
on_NtQueryPerformanceCounter_enter_t: Callable[['CPUState', int, int, int], None]
on_NtQueryPerformanceCounter_return_t: Callable[['CPUState', int, int, int], None]
on_NtQueryPortInformationProcess_enter_t: Callable[['CPUState', int], None]
on_NtQueryPortInformationProcess_return_t: Callable[['CPUState', int], None]
on_NtQueryQuotaInformationFile_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtQueryQuotaInformationFile_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtQuerySection_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQuerySection_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQuerySecurityAttributesToken_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtQuerySecurityAttributesToken_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtQuerySecurityObject_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQuerySecurityObject_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQuerySemaphore_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQuerySemaphore_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQuerySymbolicLinkObject_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtQuerySymbolicLinkObject_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtQuerySystemEnvironmentValueEx_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQuerySystemEnvironmentValueEx_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQuerySystemEnvironmentValue_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtQuerySystemEnvironmentValue_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtQuerySystemInformationEx_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtQuerySystemInformationEx_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtQuerySystemInformation_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtQuerySystemInformation_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtQuerySystemTime_enter_t: Callable[['CPUState', int, int], None]
on_NtQuerySystemTime_return_t: Callable[['CPUState', int, int], None]
on_NtQueryTimerResolution_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtQueryTimerResolution_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtQueryTimer_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryTimer_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryValueKey_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtQueryValueKey_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtQueryVirtualMemory_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtQueryVirtualMemory_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtQueryVolumeInformationFile_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueryVolumeInformationFile_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueueApcThreadEx_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtQueueApcThreadEx_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtQueueApcThread_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtQueueApcThread_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtRaiseException_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtRaiseException_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtRaiseHardError_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtRaiseHardError_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtReadFileScatter_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtReadFileScatter_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtReadFile_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtReadFile_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtReadOnlyEnlistment_enter_t: Callable[['CPUState', int, int, int], None]
on_NtReadOnlyEnlistment_return_t: Callable[['CPUState', int, int, int], None]
on_NtReadRequestData_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtReadRequestData_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtReadVirtualMemory_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtReadVirtualMemory_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtRecoverEnlistment_enter_t: Callable[['CPUState', int, int, int], None]
on_NtRecoverEnlistment_return_t: Callable[['CPUState', int, int, int], None]
on_NtRecoverResourceManager_enter_t: Callable[['CPUState', int, int], None]
on_NtRecoverResourceManager_return_t: Callable[['CPUState', int, int], None]
on_NtRecoverTransactionManager_enter_t: Callable[['CPUState', int, int], None]
on_NtRecoverTransactionManager_return_t: Callable[['CPUState', int, int], None]
on_NtRegisterProtocolAddressInformation_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtRegisterProtocolAddressInformation_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtRegisterThreadTerminatePort_enter_t: Callable[['CPUState', int, int], None]
on_NtRegisterThreadTerminatePort_return_t: Callable[['CPUState', int, int], None]
on_NtReleaseKeyedEvent_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtReleaseKeyedEvent_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtReleaseMutant_enter_t: Callable[['CPUState', int, int, int], None]
on_NtReleaseMutant_return_t: Callable[['CPUState', int, int, int], None]
on_NtReleaseSemaphore_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtReleaseSemaphore_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtReleaseWorkerFactoryWorker_enter_t: Callable[['CPUState', int, int], None]
on_NtReleaseWorkerFactoryWorker_return_t: Callable[['CPUState', int, int], None]
on_NtRemoveIoCompletionEx_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtRemoveIoCompletionEx_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtRemoveIoCompletion_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtRemoveIoCompletion_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtRemoveProcessDebug_enter_t: Callable[['CPUState', int, int, int], None]
on_NtRemoveProcessDebug_return_t: Callable[['CPUState', int, int, int], None]
on_NtRenameKey_enter_t: Callable[['CPUState', int, int, int], None]
on_NtRenameKey_return_t: Callable[['CPUState', int, int, int], None]
on_NtRenameTransactionManager_enter_t: Callable[['CPUState', int, int, int], None]
on_NtRenameTransactionManager_return_t: Callable[['CPUState', int, int, int], None]
on_NtReplaceKey_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtReplaceKey_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtReplacePartitionUnit_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtReplacePartitionUnit_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtReplyPort_enter_t: Callable[['CPUState', int, int, int], None]
on_NtReplyPort_return_t: Callable[['CPUState', int, int, int], None]
on_NtReplyWaitReceivePortEx_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtReplyWaitReceivePortEx_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtReplyWaitReceivePort_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtReplyWaitReceivePort_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtReplyWaitReplyPort_enter_t: Callable[['CPUState', int, int, int], None]
on_NtReplyWaitReplyPort_return_t: Callable[['CPUState', int, int, int], None]
on_NtRequestPort_enter_t: Callable[['CPUState', int, int, int], None]
on_NtRequestPort_return_t: Callable[['CPUState', int, int, int], None]
on_NtRequestWaitReplyPort_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtRequestWaitReplyPort_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtResetEvent_enter_t: Callable[['CPUState', int, int, int], None]
on_NtResetEvent_return_t: Callable[['CPUState', int, int, int], None]
on_NtResetWriteWatch_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtResetWriteWatch_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtRestoreKey_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtRestoreKey_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtResumeProcess_enter_t: Callable[['CPUState', int, int], None]
on_NtResumeProcess_return_t: Callable[['CPUState', int, int], None]
on_NtResumeThread_enter_t: Callable[['CPUState', int, int, int], None]
on_NtResumeThread_return_t: Callable[['CPUState', int, int, int], None]
on_NtRollbackComplete_enter_t: Callable[['CPUState', int, int, int], None]
on_NtRollbackComplete_return_t: Callable[['CPUState', int, int, int], None]
on_NtRollbackEnlistment_enter_t: Callable[['CPUState', int, int, int], None]
on_NtRollbackEnlistment_return_t: Callable[['CPUState', int, int, int], None]
on_NtRollbackTransaction_enter_t: Callable[['CPUState', int, int, int], None]
on_NtRollbackTransaction_return_t: Callable[['CPUState', int, int, int], None]
on_NtRollforwardTransactionManager_enter_t: Callable[['CPUState', int, int, int], None]
on_NtRollforwardTransactionManager_return_t: Callable[['CPUState', int, int, int], None]
on_NtSaveKeyEx_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtSaveKeyEx_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtSaveKey_enter_t: Callable[['CPUState', int, int, int], None]
on_NtSaveKey_return_t: Callable[['CPUState', int, int, int], None]
on_NtSaveMergedKeys_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtSaveMergedKeys_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtSecureConnectPort_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtSecureConnectPort_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtSerializeBoot_enter_t: Callable[['CPUState', int], None]
on_NtSerializeBoot_return_t: Callable[['CPUState', int], None]
on_NtSetBootEntryOrder_enter_t: Callable[['CPUState', int, int, int], None]
on_NtSetBootEntryOrder_return_t: Callable[['CPUState', int, int, int], None]
on_NtSetBootOptions_enter_t: Callable[['CPUState', int, int, int], None]
on_NtSetBootOptions_return_t: Callable[['CPUState', int, int, int], None]
on_NtSetContextThread_enter_t: Callable[['CPUState', int, int, int], None]
on_NtSetContextThread_return_t: Callable[['CPUState', int, int, int], None]
on_NtSetDebugFilterState_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtSetDebugFilterState_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtSetDefaultHardErrorPort_enter_t: Callable[['CPUState', int, int], None]
on_NtSetDefaultHardErrorPort_return_t: Callable[['CPUState', int, int], None]
on_NtSetDefaultLocale_enter_t: Callable[['CPUState', int, int, int], None]
on_NtSetDefaultLocale_return_t: Callable[['CPUState', int, int, int], None]
on_NtSetDefaultUILanguage_enter_t: Callable[['CPUState', int, int], None]
on_NtSetDefaultUILanguage_return_t: Callable[['CPUState', int, int], None]
on_NtSetDriverEntryOrder_enter_t: Callable[['CPUState', int, int, int], None]
on_NtSetDriverEntryOrder_return_t: Callable[['CPUState', int, int, int], None]
on_NtSetEaFile_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetEaFile_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetEventBoostPriority_enter_t: Callable[['CPUState', int, int], None]
on_NtSetEventBoostPriority_return_t: Callable[['CPUState', int, int], None]
on_NtSetEvent_enter_t: Callable[['CPUState', int, int, int], None]
on_NtSetEvent_return_t: Callable[['CPUState', int, int, int], None]
on_NtSetHighEventPair_enter_t: Callable[['CPUState', int, int], None]
on_NtSetHighEventPair_return_t: Callable[['CPUState', int, int], None]
on_NtSetHighWaitLowEventPair_enter_t: Callable[['CPUState', int, int], None]
on_NtSetHighWaitLowEventPair_return_t: Callable[['CPUState', int, int], None]
on_NtSetInformationDebugObject_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtSetInformationDebugObject_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtSetInformationEnlistment_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationEnlistment_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationFile_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtSetInformationFile_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtSetInformationJobObject_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationJobObject_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationKey_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationKey_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationObject_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationObject_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationProcess_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationProcess_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationResourceManager_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationResourceManager_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationThread_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationThread_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationToken_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationToken_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationTransactionManager_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationTransactionManager_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationTransaction_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationTransaction_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationWorkerFactory_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetInformationWorkerFactory_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetIntervalProfile_enter_t: Callable[['CPUState', int, int, int], None]
on_NtSetIntervalProfile_return_t: Callable[['CPUState', int, int, int], None]
on_NtSetIoCompletionEx_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtSetIoCompletionEx_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtSetIoCompletion_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtSetIoCompletion_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtSetLdtEntries_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtSetLdtEntries_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtSetLowEventPair_enter_t: Callable[['CPUState', int, int], None]
on_NtSetLowEventPair_return_t: Callable[['CPUState', int, int], None]
on_NtSetLowWaitHighEventPair_enter_t: Callable[['CPUState', int, int], None]
on_NtSetLowWaitHighEventPair_return_t: Callable[['CPUState', int, int], None]
on_NtSetQuotaInformationFile_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetQuotaInformationFile_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetSecurityObject_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtSetSecurityObject_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtSetSystemEnvironmentValueEx_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtSetSystemEnvironmentValueEx_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtSetSystemEnvironmentValue_enter_t: Callable[['CPUState', int, int, int], None]
on_NtSetSystemEnvironmentValue_return_t: Callable[['CPUState', int, int, int], None]
on_NtSetSystemInformation_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtSetSystemInformation_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtSetSystemPowerState_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtSetSystemPowerState_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtSetSystemTime_enter_t: Callable[['CPUState', int, int, int], None]
on_NtSetSystemTime_return_t: Callable[['CPUState', int, int, int], None]
on_NtSetThreadExecutionState_enter_t: Callable[['CPUState', int, int, int], None]
on_NtSetThreadExecutionState_return_t: Callable[['CPUState', int, int, int], None]
on_NtSetTimerEx_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetTimerEx_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSetTimerResolution_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtSetTimerResolution_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtSetTimer_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtSetTimer_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_NtSetUuidSeed_enter_t: Callable[['CPUState', int, int], None]
on_NtSetUuidSeed_return_t: Callable[['CPUState', int, int], None]
on_NtSetValueKey_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtSetValueKey_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtSetVolumeInformationFile_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtSetVolumeInformationFile_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtShutdownSystem_enter_t: Callable[['CPUState', int, int], None]
on_NtShutdownSystem_return_t: Callable[['CPUState', int, int], None]
on_NtShutdownWorkerFactory_enter_t: Callable[['CPUState', int, int, int], None]
on_NtShutdownWorkerFactory_return_t: Callable[['CPUState', int, int, int], None]
on_NtSignalAndWaitForSingleObject_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSignalAndWaitForSingleObject_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtSinglePhaseReject_enter_t: Callable[['CPUState', int, int, int], None]
on_NtSinglePhaseReject_return_t: Callable[['CPUState', int, int, int], None]
on_NtStartProfile_enter_t: Callable[['CPUState', int, int], None]
on_NtStartProfile_return_t: Callable[['CPUState', int, int], None]
on_NtStopProfile_enter_t: Callable[['CPUState', int, int], None]
on_NtStopProfile_return_t: Callable[['CPUState', int, int], None]
on_NtSuspendProcess_enter_t: Callable[['CPUState', int, int], None]
on_NtSuspendProcess_return_t: Callable[['CPUState', int, int], None]
on_NtSuspendThread_enter_t: Callable[['CPUState', int, int, int], None]
on_NtSuspendThread_return_t: Callable[['CPUState', int, int, int], None]
on_NtSystemDebugControl_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtSystemDebugControl_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtTerminateJobObject_enter_t: Callable[['CPUState', int, int, int], None]
on_NtTerminateJobObject_return_t: Callable[['CPUState', int, int, int], None]
on_NtTerminateProcess_enter_t: Callable[['CPUState', int, int, int], None]
on_NtTerminateProcess_return_t: Callable[['CPUState', int, int, int], None]
on_NtTerminateThread_enter_t: Callable[['CPUState', int, int, int], None]
on_NtTerminateThread_return_t: Callable[['CPUState', int, int, int], None]
on_NtTestAlert_enter_t: Callable[['CPUState', int], None]
on_NtTestAlert_return_t: Callable[['CPUState', int], None]
on_NtThawRegistry_enter_t: Callable[['CPUState', int], None]
on_NtThawRegistry_return_t: Callable[['CPUState', int], None]
on_NtThawTransactions_enter_t: Callable[['CPUState', int], None]
on_NtThawTransactions_return_t: Callable[['CPUState', int], None]
on_NtTraceControl_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtTraceControl_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtTraceEvent_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtTraceEvent_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtTranslateFilePath_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtTranslateFilePath_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtUmsThreadYield_enter_t: Callable[['CPUState', int, int], None]
on_NtUmsThreadYield_return_t: Callable[['CPUState', int, int], None]
on_NtUnloadDriver_enter_t: Callable[['CPUState', int, int], None]
on_NtUnloadDriver_return_t: Callable[['CPUState', int, int], None]
on_NtUnloadKey2_enter_t: Callable[['CPUState', int, int, int], None]
on_NtUnloadKey2_return_t: Callable[['CPUState', int, int, int], None]
on_NtUnloadKeyEx_enter_t: Callable[['CPUState', int, int, int], None]
on_NtUnloadKeyEx_return_t: Callable[['CPUState', int, int, int], None]
on_NtUnloadKey_enter_t: Callable[['CPUState', int, int], None]
on_NtUnloadKey_return_t: Callable[['CPUState', int, int], None]
on_NtUnlockFile_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtUnlockFile_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtUnlockVirtualMemory_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtUnlockVirtualMemory_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtUnmapViewOfSection_enter_t: Callable[['CPUState', int, int, int], None]
on_NtUnmapViewOfSection_return_t: Callable[['CPUState', int, int, int], None]
on_NtVdmControl_enter_t: Callable[['CPUState', int, int, int], None]
on_NtVdmControl_return_t: Callable[['CPUState', int, int, int], None]
on_NtWaitForDebugEvent_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtWaitForDebugEvent_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtWaitForKeyedEvent_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtWaitForKeyedEvent_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_NtWaitForMultipleObjects32_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtWaitForMultipleObjects32_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtWaitForMultipleObjects_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtWaitForMultipleObjects_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtWaitForSingleObject_enter_t: Callable[['CPUState', int, int, int, int], None]
on_NtWaitForSingleObject_return_t: Callable[['CPUState', int, int, int, int], None]
on_NtWaitForWorkViaWorkerFactory_enter_t: Callable[['CPUState', int, int, int], None]
on_NtWaitForWorkViaWorkerFactory_return_t: Callable[['CPUState', int, int, int], None]
on_NtWaitHighEventPair_enter_t: Callable[['CPUState', int, int], None]
on_NtWaitHighEventPair_return_t: Callable[['CPUState', int, int], None]
on_NtWaitLowEventPair_enter_t: Callable[['CPUState', int, int], None]
on_NtWaitLowEventPair_return_t: Callable[['CPUState', int, int], None]
on_NtWorkerFactoryWorkerReady_enter_t: Callable[['CPUState', int, int], None]
on_NtWorkerFactoryWorkerReady_return_t: Callable[['CPUState', int, int], None]
on_NtWriteFileGather_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtWriteFileGather_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtWriteFile_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtWriteFile_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int, int, int], None]
on_NtWriteRequestData_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtWriteRequestData_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_NtWriteVirtualMemory_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtWriteVirtualMemory_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_NtYieldExecution_enter_t: Callable[['CPUState', int], None]
on_NtYieldExecution_return_t: Callable[['CPUState', int], None]
on___acl_aclcheck_fd_enter_t: Callable[['CPUState', int, int, int, int], None]
on___acl_aclcheck_fd_return_t: Callable[['CPUState', int, int, int, int], None]
on___acl_aclcheck_file_enter_t: Callable[['CPUState', int, int, int, int], None]
on___acl_aclcheck_file_return_t: Callable[['CPUState', int, int, int, int], None]
on___acl_aclcheck_link_enter_t: Callable[['CPUState', int, int, int, int], None]
on___acl_aclcheck_link_return_t: Callable[['CPUState', int, int, int, int], None]
on___acl_delete_fd_enter_t: Callable[['CPUState', int, int, int], None]
on___acl_delete_fd_return_t: Callable[['CPUState', int, int, int], None]
on___acl_delete_file_enter_t: Callable[['CPUState', int, int, int], None]
on___acl_delete_file_return_t: Callable[['CPUState', int, int, int], None]
on___acl_delete_link_enter_t: Callable[['CPUState', int, int, int], None]
on___acl_delete_link_return_t: Callable[['CPUState', int, int, int], None]
on___acl_get_fd_enter_t: Callable[['CPUState', int, int, int, int], None]
on___acl_get_fd_return_t: Callable[['CPUState', int, int, int, int], None]
on___acl_get_file_enter_t: Callable[['CPUState', int, int, int, int], None]
on___acl_get_file_return_t: Callable[['CPUState', int, int, int, int], None]
on___acl_get_link_enter_t: Callable[['CPUState', int, int, int, int], None]
on___acl_get_link_return_t: Callable[['CPUState', int, int, int, int], None]
on___acl_set_fd_enter_t: Callable[['CPUState', int, int, int, int], None]
on___acl_set_fd_return_t: Callable[['CPUState', int, int, int, int], None]
on___acl_set_file_enter_t: Callable[['CPUState', int, int, int, int], None]
on___acl_set_file_return_t: Callable[['CPUState', int, int, int, int], None]
on___acl_set_link_enter_t: Callable[['CPUState', int, int, int, int], None]
on___acl_set_link_return_t: Callable[['CPUState', int, int, int, int], None]
on___cap_rights_get_enter_t: Callable[['CPUState', int, int, int, int], None]
on___cap_rights_get_return_t: Callable[['CPUState', int, int, int, int], None]
on___getcwd_enter_t: Callable[['CPUState', int, int, int], None]
on___getcwd_return_t: Callable[['CPUState', int, int, int], None]
on___mac_execve_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on___mac_execve_return_t: Callable[['CPUState', int, int, int, int, int], None]
on___mac_get_fd_enter_t: Callable[['CPUState', int, int, int], None]
on___mac_get_fd_return_t: Callable[['CPUState', int, int, int], None]
on___mac_get_file_enter_t: Callable[['CPUState', int, int, int], None]
on___mac_get_file_return_t: Callable[['CPUState', int, int, int], None]
on___mac_get_link_enter_t: Callable[['CPUState', int, int, int], None]
on___mac_get_link_return_t: Callable[['CPUState', int, int, int], None]
on___mac_get_pid_enter_t: Callable[['CPUState', int, int, int], None]
on___mac_get_pid_return_t: Callable[['CPUState', int, int, int], None]
on___mac_get_proc_enter_t: Callable[['CPUState', int, int], None]
on___mac_get_proc_return_t: Callable[['CPUState', int, int], None]
on___mac_set_fd_enter_t: Callable[['CPUState', int, int, int], None]
on___mac_set_fd_return_t: Callable[['CPUState', int, int, int], None]
on___mac_set_file_enter_t: Callable[['CPUState', int, int, int], None]
on___mac_set_file_return_t: Callable[['CPUState', int, int, int], None]
on___mac_set_link_enter_t: Callable[['CPUState', int, int, int], None]
on___mac_set_link_return_t: Callable[['CPUState', int, int, int], None]
on___mac_set_proc_enter_t: Callable[['CPUState', int, int], None]
on___mac_set_proc_return_t: Callable[['CPUState', int, int], None]
on___realpathat_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on___realpathat_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on___semctl_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on___semctl_return_t: Callable[['CPUState', int, int, int, int, int], None]
on___setugid_enter_t: Callable[['CPUState', int, int], None]
on___setugid_return_t: Callable[['CPUState', int, int], None]
on___sysctl_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on___sysctl_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on___sysctlbyname_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on___sysctlbyname_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on__umtx_op_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on__umtx_op_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_abort2_enter_t: Callable[['CPUState', int, int, int, int], None]
on_abort2_return_t: Callable[['CPUState', int, int, int, int], None]
on_accept4_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_accept4_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_accept_enter_t: Callable[['CPUState', int, int, int, int], None]
on_accept_return_t: Callable[['CPUState', int, int, int, int], None]
on_access_enter_t: Callable[['CPUState', int, int, int], None]
on_access_return_t: Callable[['CPUState', int, int, int], None]
on_acct_enter_t: Callable[['CPUState', int, int], None]
on_acct_return_t: Callable[['CPUState', int, int], None]
on_adjtime_enter_t: Callable[['CPUState', int, int, int], None]
on_adjtime_return_t: Callable[['CPUState', int, int, int], None]
on_afs3_syscall_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_afs3_syscall_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_after_load_t: Callable[['addr_struct', int, int], None]
on_after_store_t: Callable[['addr_struct', int, int], None]
on_aio_cancel_enter_t: Callable[['CPUState', int, int, int], None]
on_aio_cancel_return_t: Callable[['CPUState', int, int, int], None]
on_aio_error_enter_t: Callable[['CPUState', int, int], None]
on_aio_error_return_t: Callable[['CPUState', int, int], None]
on_aio_fsync_enter_t: Callable[['CPUState', int, int, int], None]
on_aio_fsync_return_t: Callable[['CPUState', int, int, int], None]
on_aio_mlock_enter_t: Callable[['CPUState', int, int], None]
on_aio_mlock_return_t: Callable[['CPUState', int, int], None]
on_aio_read_enter_t: Callable[['CPUState', int, int], None]
on_aio_read_return_t: Callable[['CPUState', int, int], None]
on_aio_return_enter_t: Callable[['CPUState', int, int], None]
on_aio_return_return_t: Callable[['CPUState', int, int], None]
on_aio_suspend_enter_t: Callable[['CPUState', int, int, int, int], None]
on_aio_suspend_return_t: Callable[['CPUState', int, int, int, int], None]
on_aio_waitcomplete_enter_t: Callable[['CPUState', int, int, int], None]
on_aio_waitcomplete_return_t: Callable[['CPUState', int, int, int], None]
on_aio_write_enter_t: Callable[['CPUState', int, int], None]
on_aio_write_return_t: Callable[['CPUState', int, int], None]
on_all_sys_enter2_t: Callable[['CPUState', int, 'syscall_info_t', 'syscall_ctx'], None]
on_all_sys_enter_t: Callable[['CPUState', int, int], None]
on_all_sys_return2_t: Callable[['CPUState', int, 'syscall_info_t', 'syscall_ctx'], None]
on_all_sys_return_t: Callable[['CPUState', int, int], None]
on_audit_enter_t: Callable[['CPUState', int, int, int], None]
on_audit_return_t: Callable[['CPUState', int, int, int], None]
on_auditctl_enter_t: Callable[['CPUState', int, int], None]
on_auditctl_return_t: Callable[['CPUState', int, int], None]
on_auditon_enter_t: Callable[['CPUState', int, int, int, int], None]
on_auditon_return_t: Callable[['CPUState', int, int, int, int], None]
on_bind_enter_t: Callable[['CPUState', int, int, int, int], None]
on_bind_return_t: Callable[['CPUState', int, int, int, int], None]
on_bindat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_bindat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_branch2_t: Callable[['addr_struct', int, bool, bool], None]
on_branch_t: Callable[['CPUState', 'TranslationBlock', int], bool]
on_call_match_num_t: Callable[['CPUState', int, int, int, int], None]
on_call_match_str_t: Callable[['CPUState', int, int, bytes, int, int], None]
on_call_t: Callable[['CPUState', int], None]
on_cap_enter_enter_t: Callable[['CPUState', int], None]
on_cap_enter_return_t: Callable[['CPUState', int], None]
on_cap_fcntls_get_enter_t: Callable[['CPUState', int, int, int], None]
on_cap_fcntls_get_return_t: Callable[['CPUState', int, int, int], None]
on_cap_fcntls_limit_enter_t: Callable[['CPUState', int, int, int], None]
on_cap_fcntls_limit_return_t: Callable[['CPUState', int, int, int], None]
on_cap_getmode_enter_t: Callable[['CPUState', int, int], None]
on_cap_getmode_return_t: Callable[['CPUState', int, int], None]
on_cap_ioctls_get_enter_t: Callable[['CPUState', int, int, int, int], None]
on_cap_ioctls_get_return_t: Callable[['CPUState', int, int, int, int], None]
on_cap_ioctls_limit_enter_t: Callable[['CPUState', int, int, int, int], None]
on_cap_ioctls_limit_return_t: Callable[['CPUState', int, int, int, int], None]
on_cap_rights_limit_enter_t: Callable[['CPUState', int, int, int], None]
on_cap_rights_limit_return_t: Callable[['CPUState', int, int, int], None]
on_chdir_enter_t: Callable[['CPUState', int, int], None]
on_chdir_return_t: Callable[['CPUState', int, int], None]
on_chflags_enter_t: Callable[['CPUState', int, int, int], None]
on_chflags_return_t: Callable[['CPUState', int, int, int], None]
on_chflagsat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_chflagsat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_chmod_enter_t: Callable[['CPUState', int, int, int], None]
on_chmod_return_t: Callable[['CPUState', int, int, int], None]
on_chown_enter_t: Callable[['CPUState', int, int, int, int], None]
on_chown_return_t: Callable[['CPUState', int, int, int, int], None]
on_chroot_enter_t: Callable[['CPUState', int, int], None]
on_chroot_return_t: Callable[['CPUState', int, int], None]
on_clock_getcpuclockid2_enter_t: Callable[['CPUState', int, int, int, int], None]
on_clock_getcpuclockid2_return_t: Callable[['CPUState', int, int, int, int], None]
on_clock_getres_enter_t: Callable[['CPUState', int, int, int], None]
on_clock_getres_return_t: Callable[['CPUState', int, int, int], None]
on_clock_gettime_enter_t: Callable[['CPUState', int, int, int], None]
on_clock_gettime_return_t: Callable[['CPUState', int, int, int], None]
on_clock_nanosleep_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_clock_nanosleep_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_clock_settime_enter_t: Callable[['CPUState', int, int, int], None]
on_clock_settime_return_t: Callable[['CPUState', int, int, int], None]
on_close_enter_t: Callable[['CPUState', int, int], None]
on_close_range_enter_t: Callable[['CPUState', int, int, int, int], None]
on_close_range_return_t: Callable[['CPUState', int, int, int, int], None]
on_close_return_t: Callable[['CPUState', int, int], None]
on_closefrom_enter_t: Callable[['CPUState', int, int], None]
on_closefrom_return_t: Callable[['CPUState', int, int], None]
on_connect_enter_t: Callable[['CPUState', int, int, int, int], None]
on_connect_return_t: Callable[['CPUState', int, int, int, int], None]
on_connectat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_connectat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_copy_file_range_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_copy_file_range_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_cpuset_enter_t: Callable[['CPUState', int, int], None]
on_cpuset_getaffinity_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_cpuset_getaffinity_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_cpuset_getdomain_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_cpuset_getdomain_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_cpuset_getid_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_cpuset_getid_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_cpuset_return_t: Callable[['CPUState', int, int], None]
on_cpuset_setaffinity_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_cpuset_setaffinity_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_cpuset_setdomain_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_cpuset_setdomain_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_cpuset_setid_enter_t: Callable[['CPUState', int, int, int, int], None]
on_cpuset_setid_return_t: Callable[['CPUState', int, int, int, int], None]
on_creat_enter_t: Callable[['CPUState', int, int, int], None]
on_creat_return_t: Callable[['CPUState', int, int, int], None]
on_dup2_enter_t: Callable[['CPUState', int, int, int], None]
on_dup2_return_t: Callable[['CPUState', int, int, int], None]
on_dup_enter_t: Callable[['CPUState', int, int], None]
on_dup_return_t: Callable[['CPUState', int, int], None]
on_eaccess_enter_t: Callable[['CPUState', int, int, int], None]
on_eaccess_return_t: Callable[['CPUState', int, int, int], None]
on_execve_enter_t: Callable[['CPUState', int, int, int, int], None]
on_execve_return_t: Callable[['CPUState', int, int, int, int], None]
on_extattr_delete_fd_enter_t: Callable[['CPUState', int, int, int, int], None]
on_extattr_delete_fd_return_t: Callable[['CPUState', int, int, int, int], None]
on_extattr_delete_file_enter_t: Callable[['CPUState', int, int, int, int], None]
on_extattr_delete_file_return_t: Callable[['CPUState', int, int, int, int], None]
on_extattr_delete_link_enter_t: Callable[['CPUState', int, int, int, int], None]
on_extattr_delete_link_return_t: Callable[['CPUState', int, int, int, int], None]
on_extattr_get_fd_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_extattr_get_fd_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_extattr_get_file_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_extattr_get_file_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_extattr_get_link_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_extattr_get_link_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_extattr_list_fd_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_extattr_list_fd_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_extattr_list_file_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_extattr_list_file_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_extattr_list_link_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_extattr_list_link_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_extattr_set_fd_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_extattr_set_fd_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_extattr_set_file_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_extattr_set_file_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_extattr_set_link_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_extattr_set_link_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_extattrctl_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_extattrctl_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_faccessat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_faccessat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_fchdir_enter_t: Callable[['CPUState', int, int], None]
on_fchdir_return_t: Callable[['CPUState', int, int], None]
on_fchflags_enter_t: Callable[['CPUState', int, int, int], None]
on_fchflags_return_t: Callable[['CPUState', int, int, int], None]
on_fchmod_enter_t: Callable[['CPUState', int, int, int], None]
on_fchmod_return_t: Callable[['CPUState', int, int, int], None]
on_fchmodat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_fchmodat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_fchown_enter_t: Callable[['CPUState', int, int, int, int], None]
on_fchown_return_t: Callable[['CPUState', int, int, int, int], None]
on_fchownat_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_fchownat_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_fcntl_enter_t: Callable[['CPUState', int, int, int, int], None]
on_fcntl_return_t: Callable[['CPUState', int, int, int, int], None]
on_fdatasync_enter_t: Callable[['CPUState', int, int], None]
on_fdatasync_return_t: Callable[['CPUState', int, int], None]
on_fexecve_enter_t: Callable[['CPUState', int, int, int, int], None]
on_fexecve_return_t: Callable[['CPUState', int, int, int, int], None]
on_ffclock_getcounter_enter_t: Callable[['CPUState', int, int], None]
on_ffclock_getcounter_return_t: Callable[['CPUState', int, int], None]
on_ffclock_getestimate_enter_t: Callable[['CPUState', int, int], None]
on_ffclock_getestimate_return_t: Callable[['CPUState', int, int], None]
on_ffclock_setestimate_enter_t: Callable[['CPUState', int, int], None]
on_ffclock_setestimate_return_t: Callable[['CPUState', int, int], None]
on_fhlink_enter_t: Callable[['CPUState', int, int, int], None]
on_fhlink_return_t: Callable[['CPUState', int, int, int], None]
on_fhlinkat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_fhlinkat_return_t: Callable[['CPUState', int, int, int, int], None]
on_fhopen_enter_t: Callable[['CPUState', int, int, int], None]
on_fhopen_return_t: Callable[['CPUState', int, int, int], None]
on_fhreadlink_enter_t: Callable[['CPUState', int, int, int, int], None]
on_fhreadlink_return_t: Callable[['CPUState', int, int, int, int], None]
on_fhstat_enter_t: Callable[['CPUState', int, int, int], None]
on_fhstat_return_t: Callable[['CPUState', int, int, int], None]
on_fhstatfs_enter_t: Callable[['CPUState', int, int, int], None]
on_fhstatfs_return_t: Callable[['CPUState', int, int, int], None]
on_flock_enter_t: Callable[['CPUState', int, int, int], None]
on_flock_return_t: Callable[['CPUState', int, int, int], None]
on_fork_enter_t: Callable[['CPUState', int], None]
on_fork_return_t: Callable[['CPUState', int], None]
on_fpathconf_enter_t: Callable[['CPUState', int, int, int], None]
on_fpathconf_return_t: Callable[['CPUState', int, int, int], None]
on_fstat_enter_t: Callable[['CPUState', int, int, int], None]
on_fstat_return_t: Callable[['CPUState', int, int, int], None]
on_fstatat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_fstatat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_fstatfs_enter_t: Callable[['CPUState', int, int, int], None]
on_fstatfs_return_t: Callable[['CPUState', int, int, int], None]
on_fsync_enter_t: Callable[['CPUState', int, int], None]
on_fsync_return_t: Callable[['CPUState', int, int], None]
on_ftruncate_enter_t: Callable[['CPUState', int, int, int], None]
on_ftruncate_return_t: Callable[['CPUState', int, int, int], None]
on_funlinkat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_funlinkat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_futimens_enter_t: Callable[['CPUState', int, int, int], None]
on_futimens_return_t: Callable[['CPUState', int, int, int], None]
on_futimes_enter_t: Callable[['CPUState', int, int, int], None]
on_futimes_return_t: Callable[['CPUState', int, int, int], None]
on_futimesat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_futimesat_return_t: Callable[['CPUState', int, int, int, int], None]
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
on_getaudit_addr_enter_t: Callable[['CPUState', int, int, int], None]
on_getaudit_addr_return_t: Callable[['CPUState', int, int, int], None]
on_getaudit_enter_t: Callable[['CPUState', int, int], None]
on_getaudit_return_t: Callable[['CPUState', int, int], None]
on_getauid_enter_t: Callable[['CPUState', int, int], None]
on_getauid_return_t: Callable[['CPUState', int, int], None]
on_getcontext_enter_t: Callable[['CPUState', int, int], None]
on_getcontext_return_t: Callable[['CPUState', int, int], None]
on_getdents_enter_t: Callable[['CPUState', int, int, int, int], None]
on_getdents_return_t: Callable[['CPUState', int, int, int, int], None]
on_getdirentries_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_getdirentries_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_getdomainname_enter_t: Callable[['CPUState', int, int, int], None]
on_getdomainname_return_t: Callable[['CPUState', int, int, int], None]
on_getdtablesize_enter_t: Callable[['CPUState', int], None]
on_getdtablesize_return_t: Callable[['CPUState', int], None]
on_getegid_enter_t: Callable[['CPUState', int], None]
on_getegid_return_t: Callable[['CPUState', int], None]
on_geteuid_enter_t: Callable[['CPUState', int], None]
on_geteuid_return_t: Callable[['CPUState', int], None]
on_getfh_enter_t: Callable[['CPUState', int, int, int], None]
on_getfh_return_t: Callable[['CPUState', int, int, int], None]
on_getfhat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_getfhat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_getfsstat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_getfsstat_return_t: Callable[['CPUState', int, int, int, int], None]
on_getgid_enter_t: Callable[['CPUState', int], None]
on_getgid_return_t: Callable[['CPUState', int], None]
on_getgroups_enter_t: Callable[['CPUState', int, int, int], None]
on_getgroups_return_t: Callable[['CPUState', int, int, int], None]
on_gethostid_enter_t: Callable[['CPUState', int], None]
on_gethostid_return_t: Callable[['CPUState', int], None]
on_gethostname_enter_t: Callable[['CPUState', int, int, int], None]
on_gethostname_return_t: Callable[['CPUState', int, int, int], None]
on_getitimer_enter_t: Callable[['CPUState', int, int, int], None]
on_getitimer_return_t: Callable[['CPUState', int, int, int], None]
on_getkerninfo_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_getkerninfo_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_getlogin_enter_t: Callable[['CPUState', int, int, int], None]
on_getlogin_return_t: Callable[['CPUState', int, int, int], None]
on_getloginclass_enter_t: Callable[['CPUState', int, int, int], None]
on_getloginclass_return_t: Callable[['CPUState', int, int, int], None]
on_getpagesize_enter_t: Callable[['CPUState', int], None]
on_getpagesize_return_t: Callable[['CPUState', int], None]
on_getpeername_enter_t: Callable[['CPUState', int, int, int, int], None]
on_getpeername_return_t: Callable[['CPUState', int, int, int, int], None]
on_getpgid_enter_t: Callable[['CPUState', int, int], None]
on_getpgid_return_t: Callable[['CPUState', int, int], None]
on_getpgrp_enter_t: Callable[['CPUState', int], None]
on_getpgrp_return_t: Callable[['CPUState', int], None]
on_getpid_enter_t: Callable[['CPUState', int], None]
on_getpid_return_t: Callable[['CPUState', int], None]
on_getppid_enter_t: Callable[['CPUState', int], None]
on_getppid_return_t: Callable[['CPUState', int], None]
on_getpriority_enter_t: Callable[['CPUState', int, int, int], None]
on_getpriority_return_t: Callable[['CPUState', int, int, int], None]
on_getrandom_enter_t: Callable[['CPUState', int, int, int, int], None]
on_getrandom_return_t: Callable[['CPUState', int, int, int, int], None]
on_getresgid_enter_t: Callable[['CPUState', int, int, int, int], None]
on_getresgid_return_t: Callable[['CPUState', int, int, int, int], None]
on_getresuid_enter_t: Callable[['CPUState', int, int, int, int], None]
on_getresuid_return_t: Callable[['CPUState', int, int, int, int], None]
on_getrlimit_enter_t: Callable[['CPUState', int, int, int], None]
on_getrlimit_return_t: Callable[['CPUState', int, int, int], None]
on_getrusage_enter_t: Callable[['CPUState', int, int, int], None]
on_getrusage_return_t: Callable[['CPUState', int, int, int], None]
on_getsid_enter_t: Callable[['CPUState', int, int], None]
on_getsid_return_t: Callable[['CPUState', int, int], None]
on_getsockname_enter_t: Callable[['CPUState', int, int, int, int], None]
on_getsockname_return_t: Callable[['CPUState', int, int, int, int], None]
on_getsockopt_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_getsockopt_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_gettimeofday_enter_t: Callable[['CPUState', int, int, int], None]
on_gettimeofday_return_t: Callable[['CPUState', int, int, int], None]
on_getuid_enter_t: Callable[['CPUState', int], None]
on_getuid_return_t: Callable[['CPUState', int], None]
on_gssd_syscall_enter_t: Callable[['CPUState', int, int], None]
on_gssd_syscall_return_t: Callable[['CPUState', int, int], None]
on_has_mapping_prefix_t: Callable[['CPUState', 'osi_proc_struct', bytes, bool], None]
on_indirect_jump_t: Callable[['addr_struct', int, bool, bool], None]
on_ioctl_enter_t: Callable[['CPUState', int, int, int, int], None]
on_ioctl_return_t: Callable[['CPUState', int, int, int, int], None]
on_issetugid_enter_t: Callable[['CPUState', int], None]
on_issetugid_return_t: Callable[['CPUState', int], None]
on_jail_attach_enter_t: Callable[['CPUState', int, int], None]
on_jail_attach_return_t: Callable[['CPUState', int, int], None]
on_jail_enter_t: Callable[['CPUState', int, int], None]
on_jail_get_enter_t: Callable[['CPUState', int, int, int, int], None]
on_jail_get_return_t: Callable[['CPUState', int, int, int, int], None]
on_jail_remove_enter_t: Callable[['CPUState', int, int], None]
on_jail_remove_return_t: Callable[['CPUState', int, int], None]
on_jail_return_t: Callable[['CPUState', int, int], None]
on_jail_set_enter_t: Callable[['CPUState', int, int, int, int], None]
on_jail_set_return_t: Callable[['CPUState', int, int, int, int], None]
on_kenv_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_kenv_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_kevent_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_kevent_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_kill_enter_t: Callable[['CPUState', int, int, int], None]
on_kill_return_t: Callable[['CPUState', int, int, int], None]
on_killpg_enter_t: Callable[['CPUState', int, int, int], None]
on_killpg_return_t: Callable[['CPUState', int, int, int], None]
on_kldfind_enter_t: Callable[['CPUState', int, int], None]
on_kldfind_return_t: Callable[['CPUState', int, int], None]
on_kldfirstmod_enter_t: Callable[['CPUState', int, int], None]
on_kldfirstmod_return_t: Callable[['CPUState', int, int], None]
on_kldload_enter_t: Callable[['CPUState', int, int], None]
on_kldload_return_t: Callable[['CPUState', int, int], None]
on_kldnext_enter_t: Callable[['CPUState', int, int], None]
on_kldnext_return_t: Callable[['CPUState', int, int], None]
on_kldstat_enter_t: Callable[['CPUState', int, int, int], None]
on_kldstat_return_t: Callable[['CPUState', int, int, int], None]
on_kldsym_enter_t: Callable[['CPUState', int, int, int, int], None]
on_kldsym_return_t: Callable[['CPUState', int, int, int, int], None]
on_kldunload_enter_t: Callable[['CPUState', int, int], None]
on_kldunload_return_t: Callable[['CPUState', int, int], None]
on_kldunloadf_enter_t: Callable[['CPUState', int, int, int], None]
on_kldunloadf_return_t: Callable[['CPUState', int, int, int], None]
on_kmq_notify_enter_t: Callable[['CPUState', int, int, int], None]
on_kmq_notify_return_t: Callable[['CPUState', int, int, int], None]
on_kmq_open_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_kmq_open_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_kmq_setattr_enter_t: Callable[['CPUState', int, int, int, int], None]
on_kmq_setattr_return_t: Callable[['CPUState', int, int, int, int], None]
on_kmq_timedreceive_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_kmq_timedreceive_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_kmq_timedsend_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_kmq_timedsend_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_kmq_unlink_enter_t: Callable[['CPUState', int, int], None]
on_kmq_unlink_return_t: Callable[['CPUState', int, int], None]
on_kqueue_enter_t: Callable[['CPUState', int], None]
on_kqueue_return_t: Callable[['CPUState', int], None]
on_ksem_close_enter_t: Callable[['CPUState', int, int], None]
on_ksem_close_return_t: Callable[['CPUState', int, int], None]
on_ksem_destroy_enter_t: Callable[['CPUState', int, int], None]
on_ksem_destroy_return_t: Callable[['CPUState', int, int], None]
on_ksem_getvalue_enter_t: Callable[['CPUState', int, int, int], None]
on_ksem_getvalue_return_t: Callable[['CPUState', int, int, int], None]
on_ksem_init_enter_t: Callable[['CPUState', int, int, int], None]
on_ksem_init_return_t: Callable[['CPUState', int, int, int], None]
on_ksem_open_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_ksem_open_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_ksem_post_enter_t: Callable[['CPUState', int, int], None]
on_ksem_post_return_t: Callable[['CPUState', int, int], None]
on_ksem_timedwait_enter_t: Callable[['CPUState', int, int, int], None]
on_ksem_timedwait_return_t: Callable[['CPUState', int, int, int], None]
on_ksem_trywait_enter_t: Callable[['CPUState', int, int], None]
on_ksem_trywait_return_t: Callable[['CPUState', int, int], None]
on_ksem_unlink_enter_t: Callable[['CPUState', int, int], None]
on_ksem_unlink_return_t: Callable[['CPUState', int, int], None]
on_ksem_wait_enter_t: Callable[['CPUState', int, int], None]
on_ksem_wait_return_t: Callable[['CPUState', int, int], None]
on_ktimer_create_enter_t: Callable[['CPUState', int, int, int, int], None]
on_ktimer_create_return_t: Callable[['CPUState', int, int, int, int], None]
on_ktimer_delete_enter_t: Callable[['CPUState', int, int], None]
on_ktimer_delete_return_t: Callable[['CPUState', int, int], None]
on_ktimer_getoverrun_enter_t: Callable[['CPUState', int, int], None]
on_ktimer_getoverrun_return_t: Callable[['CPUState', int, int], None]
on_ktimer_gettime_enter_t: Callable[['CPUState', int, int, int], None]
on_ktimer_gettime_return_t: Callable[['CPUState', int, int, int], None]
on_ktimer_settime_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_ktimer_settime_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_ktrace_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_ktrace_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_lchflags_enter_t: Callable[['CPUState', int, int, int], None]
on_lchflags_return_t: Callable[['CPUState', int, int, int], None]
on_lchmod_enter_t: Callable[['CPUState', int, int, int], None]
on_lchmod_return_t: Callable[['CPUState', int, int, int], None]
on_lchown_enter_t: Callable[['CPUState', int, int, int, int], None]
on_lchown_return_t: Callable[['CPUState', int, int, int, int], None]
on_lgetfh_enter_t: Callable[['CPUState', int, int, int], None]
on_lgetfh_return_t: Callable[['CPUState', int, int, int], None]
on_link_enter_t: Callable[['CPUState', int, int, int], None]
on_link_return_t: Callable[['CPUState', int, int, int], None]
on_linkat_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_linkat_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_lio_listio_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_lio_listio_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_listen_enter_t: Callable[['CPUState', int, int, int], None]
on_listen_return_t: Callable[['CPUState', int, int, int], None]
on_lpathconf_enter_t: Callable[['CPUState', int, int, int], None]
on_lpathconf_return_t: Callable[['CPUState', int, int, int], None]
on_lseek_enter_t: Callable[['CPUState', int, int, int, int], None]
on_lseek_return_t: Callable[['CPUState', int, int, int, int], None]
on_lstat_enter_t: Callable[['CPUState', int, int, int], None]
on_lstat_return_t: Callable[['CPUState', int, int, int], None]
on_lutimes_enter_t: Callable[['CPUState', int, int, int], None]
on_lutimes_return_t: Callable[['CPUState', int, int, int], None]
on_mac_syscall_enter_t: Callable[['CPUState', int, int, int, int], None]
on_mac_syscall_return_t: Callable[['CPUState', int, int, int, int], None]
on_madvise_enter_t: Callable[['CPUState', int, int, int, int], None]
on_madvise_return_t: Callable[['CPUState', int, int, int, int], None]
on_mincore_enter_t: Callable[['CPUState', int, int, int, int], None]
on_mincore_return_t: Callable[['CPUState', int, int, int, int], None]
on_minherit_enter_t: Callable[['CPUState', int, int, int, int], None]
on_minherit_return_t: Callable[['CPUState', int, int, int, int], None]
on_mkdir_enter_t: Callable[['CPUState', int, int, int], None]
on_mkdir_return_t: Callable[['CPUState', int, int, int], None]
on_mkdirat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_mkdirat_return_t: Callable[['CPUState', int, int, int, int], None]
on_mkfifo_enter_t: Callable[['CPUState', int, int, int], None]
on_mkfifo_return_t: Callable[['CPUState', int, int, int], None]
on_mkfifoat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_mkfifoat_return_t: Callable[['CPUState', int, int, int, int], None]
on_mknod_enter_t: Callable[['CPUState', int, int, int, int], None]
on_mknod_return_t: Callable[['CPUState', int, int, int, int], None]
on_mknodat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_mknodat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_mlock_enter_t: Callable[['CPUState', int, int, int], None]
on_mlock_return_t: Callable[['CPUState', int, int, int], None]
on_mlockall_enter_t: Callable[['CPUState', int, int], None]
on_mlockall_return_t: Callable[['CPUState', int, int], None]
on_mmap_updated_t: Callable[['CPUState', bytes, int, int], None]
on_modfind_enter_t: Callable[['CPUState', int, int], None]
on_modfind_return_t: Callable[['CPUState', int, int], None]
on_modfnext_enter_t: Callable[['CPUState', int, int], None]
on_modfnext_return_t: Callable[['CPUState', int, int], None]
on_modnext_enter_t: Callable[['CPUState', int, int], None]
on_modnext_return_t: Callable[['CPUState', int, int], None]
on_modstat_enter_t: Callable[['CPUState', int, int, int], None]
on_modstat_return_t: Callable[['CPUState', int, int, int], None]
on_mount_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_mount_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_mprotect_enter_t: Callable[['CPUState', int, int, int, int], None]
on_mprotect_return_t: Callable[['CPUState', int, int, int, int], None]
on_msgctl_enter_t: Callable[['CPUState', int, int, int, int], None]
on_msgctl_return_t: Callable[['CPUState', int, int, int, int], None]
on_msgget_enter_t: Callable[['CPUState', int, int, int], None]
on_msgget_return_t: Callable[['CPUState', int, int, int], None]
on_msgrcv_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_msgrcv_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_msgsnd_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_msgsnd_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_msync_enter_t: Callable[['CPUState', int, int, int, int], None]
on_msync_return_t: Callable[['CPUState', int, int, int, int], None]
on_munlock_enter_t: Callable[['CPUState', int, int, int], None]
on_munlock_return_t: Callable[['CPUState', int, int, int], None]
on_munmap_enter_t: Callable[['CPUState', int, int, int], None]
on_munmap_return_t: Callable[['CPUState', int, int, int], None]
on_nanosleep_enter_t: Callable[['CPUState', int, int, int], None]
on_nanosleep_return_t: Callable[['CPUState', int, int, int], None]
on_nfssvc_enter_t: Callable[['CPUState', int, int, int], None]
on_nfssvc_return_t: Callable[['CPUState', int, int, int], None]
on_nfstat_enter_t: Callable[['CPUState', int, int, int], None]
on_nfstat_return_t: Callable[['CPUState', int, int, int], None]
on_nlm_syscall_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_nlm_syscall_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_nlstat_enter_t: Callable[['CPUState', int, int, int], None]
on_nlstat_return_t: Callable[['CPUState', int, int, int], None]
on_nmount_enter_t: Callable[['CPUState', int, int, int, int], None]
on_nmount_return_t: Callable[['CPUState', int, int, int, int], None]
on_nnpfs_syscall_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_nnpfs_syscall_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_nosys_enter_t: Callable[['CPUState', int], None]
on_nosys_return_t: Callable[['CPUState', int], None]
on_nstat_enter_t: Callable[['CPUState', int, int, int], None]
on_nstat_return_t: Callable[['CPUState', int, int, int], None]
on_ntp_adjtime_enter_t: Callable[['CPUState', int, int], None]
on_ntp_adjtime_return_t: Callable[['CPUState', int, int], None]
on_ntp_gettime_enter_t: Callable[['CPUState', int, int], None]
on_ntp_gettime_return_t: Callable[['CPUState', int, int], None]
on_open_enter_t: Callable[['CPUState', int, int, int, int], None]
on_open_return_t: Callable[['CPUState', int, int, int, int], None]
on_openat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_openat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_pathconf_enter_t: Callable[['CPUState', int, int, int], None]
on_pathconf_return_t: Callable[['CPUState', int, int, int], None]
on_pdfork_enter_t: Callable[['CPUState', int, int, int], None]
on_pdfork_return_t: Callable[['CPUState', int, int, int], None]
on_pdgetpid_enter_t: Callable[['CPUState', int, int, int], None]
on_pdgetpid_return_t: Callable[['CPUState', int, int, int], None]
on_pdkill_enter_t: Callable[['CPUState', int, int, int], None]
on_pdkill_return_t: Callable[['CPUState', int, int, int], None]
on_pipe2_enter_t: Callable[['CPUState', int, int, int], None]
on_pipe2_return_t: Callable[['CPUState', int, int, int], None]
on_pipe_enter_t: Callable[['CPUState', int], None]
on_pipe_return_t: Callable[['CPUState', int], None]
on_poll_enter_t: Callable[['CPUState', int, int, int, int], None]
on_poll_return_t: Callable[['CPUState', int, int, int, int], None]
on_posix_fadvise_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_posix_fadvise_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_posix_fallocate_enter_t: Callable[['CPUState', int, int, int, int], None]
on_posix_fallocate_return_t: Callable[['CPUState', int, int, int, int], None]
on_posix_openpt_enter_t: Callable[['CPUState', int, int], None]
on_posix_openpt_return_t: Callable[['CPUState', int, int], None]
on_ppoll_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_ppoll_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_pread_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_pread_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_preadv_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_preadv_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_procctl_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_procctl_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_process_end_t: Callable[['CPUState', bytes, int, int], None]
on_process_start_t: Callable[['CPUState', bytes, int, int], None]
on_profil_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_profil_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_pselect_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_pselect_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_ptr_load_t: Callable[['addr_struct', int, int], None]
on_ptr_store_t: Callable[['addr_struct', int, int], None]
on_ptrace_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_ptrace_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_pwrite_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_pwrite_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_pwritev_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_pwritev_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_quota_enter_t: Callable[['CPUState', int], None]
on_quota_return_t: Callable[['CPUState', int], None]
on_quotactl_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_quotactl_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_rctl_add_rule_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_rctl_add_rule_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_rctl_get_limits_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_rctl_get_limits_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_rctl_get_racct_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_rctl_get_racct_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_rctl_get_rules_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_rctl_get_rules_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_rctl_remove_rule_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_rctl_remove_rule_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_read_enter_t: Callable[['CPUState', int, int, int, int], None]
on_read_return_t: Callable[['CPUState', int, int, int, int], None]
on_readlink_enter_t: Callable[['CPUState', int, int, int, int], None]
on_readlink_return_t: Callable[['CPUState', int, int, int, int], None]
on_readlinkat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_readlinkat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_readv_enter_t: Callable[['CPUState', int, int, int, int], None]
on_readv_return_t: Callable[['CPUState', int, int, int, int], None]
on_reboot_enter_t: Callable[['CPUState', int, int], None]
on_reboot_return_t: Callable[['CPUState', int, int], None]
on_rec_auxv_t: Callable[['CPUState', 'TranslationBlock', 'auxv_values'], None]
on_recv_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_recv_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_recvfrom_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_recvfrom_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_recvmsg_enter_t: Callable[['CPUState', int, int, int, int], None]
on_recvmsg_return_t: Callable[['CPUState', int, int, int, int], None]
on_rename_enter_t: Callable[['CPUState', int, int, int], None]
on_rename_return_t: Callable[['CPUState', int, int, int], None]
on_renameat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_renameat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_ret_t: Callable[['CPUState', int], None]
on_revoke_enter_t: Callable[['CPUState', int, int], None]
on_revoke_return_t: Callable[['CPUState', int, int], None]
on_rfork_enter_t: Callable[['CPUState', int, int], None]
on_rfork_return_t: Callable[['CPUState', int, int], None]
on_rmdir_enter_t: Callable[['CPUState', int, int], None]
on_rmdir_return_t: Callable[['CPUState', int, int], None]
on_rpctls_syscall_enter_t: Callable[['CPUState', int, int, int], None]
on_rpctls_syscall_return_t: Callable[['CPUState', int, int, int], None]
on_rtprio_enter_t: Callable[['CPUState', int, int, int, int], None]
on_rtprio_return_t: Callable[['CPUState', int, int, int, int], None]
on_rtprio_thread_enter_t: Callable[['CPUState', int, int, int, int], None]
on_rtprio_thread_return_t: Callable[['CPUState', int, int, int, int], None]
on_sbrk_enter_t: Callable[['CPUState', int, int], None]
on_sbrk_return_t: Callable[['CPUState', int, int], None]
on_sched_get_priority_max_enter_t: Callable[['CPUState', int, int], None]
on_sched_get_priority_max_return_t: Callable[['CPUState', int, int], None]
on_sched_get_priority_min_enter_t: Callable[['CPUState', int, int], None]
on_sched_get_priority_min_return_t: Callable[['CPUState', int, int], None]
on_sched_getparam_enter_t: Callable[['CPUState', int, int, int], None]
on_sched_getparam_return_t: Callable[['CPUState', int, int, int], None]
on_sched_getscheduler_enter_t: Callable[['CPUState', int, int], None]
on_sched_getscheduler_return_t: Callable[['CPUState', int, int], None]
on_sched_rr_get_interval_enter_t: Callable[['CPUState', int, int, int], None]
on_sched_rr_get_interval_return_t: Callable[['CPUState', int, int, int], None]
on_sched_setparam_enter_t: Callable[['CPUState', int, int, int], None]
on_sched_setparam_return_t: Callable[['CPUState', int, int, int], None]
on_sched_setscheduler_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sched_setscheduler_return_t: Callable[['CPUState', int, int, int, int], None]
on_sched_yield_enter_t: Callable[['CPUState', int], None]
on_sched_yield_return_t: Callable[['CPUState', int], None]
on_sctp_generic_recvmsg_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_sctp_generic_recvmsg_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_sctp_generic_sendmsg_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_sctp_generic_sendmsg_iov_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_sctp_generic_sendmsg_iov_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_sctp_generic_sendmsg_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_sctp_peeloff_enter_t: Callable[['CPUState', int, int, int], None]
on_sctp_peeloff_return_t: Callable[['CPUState', int, int, int], None]
on_select_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_select_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_semget_enter_t: Callable[['CPUState', int, int, int, int], None]
on_semget_return_t: Callable[['CPUState', int, int, int, int], None]
on_semop_enter_t: Callable[['CPUState', int, int, int, int], None]
on_semop_return_t: Callable[['CPUState', int, int, int, int], None]
on_semsys_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_semsys_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_send_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_send_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sendfile_enter_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_sendfile_return_t: Callable[['CPUState', int, int, int, int, int, int, int, int], None]
on_sendmsg_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sendmsg_return_t: Callable[['CPUState', int, int, int, int], None]
on_sendto_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sendto_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_setaudit_addr_enter_t: Callable[['CPUState', int, int, int], None]
on_setaudit_addr_return_t: Callable[['CPUState', int, int, int], None]
on_setaudit_enter_t: Callable[['CPUState', int, int], None]
on_setaudit_return_t: Callable[['CPUState', int, int], None]
on_setauid_enter_t: Callable[['CPUState', int, int], None]
on_setauid_return_t: Callable[['CPUState', int, int], None]
on_setcontext_enter_t: Callable[['CPUState', int, int], None]
on_setcontext_return_t: Callable[['CPUState', int, int], None]
on_setdomainname_enter_t: Callable[['CPUState', int, int, int], None]
on_setdomainname_return_t: Callable[['CPUState', int, int, int], None]
on_setegid_enter_t: Callable[['CPUState', int, int], None]
on_setegid_return_t: Callable[['CPUState', int, int], None]
on_seteuid_enter_t: Callable[['CPUState', int, int], None]
on_seteuid_return_t: Callable[['CPUState', int, int], None]
on_setfib_enter_t: Callable[['CPUState', int, int], None]
on_setfib_return_t: Callable[['CPUState', int, int], None]
on_setgid_enter_t: Callable[['CPUState', int, int], None]
on_setgid_return_t: Callable[['CPUState', int, int], None]
on_setgroups_enter_t: Callable[['CPUState', int, int, int], None]
on_setgroups_return_t: Callable[['CPUState', int, int, int], None]
on_sethostid_enter_t: Callable[['CPUState', int, int], None]
on_sethostid_return_t: Callable[['CPUState', int, int], None]
on_sethostname_enter_t: Callable[['CPUState', int, int, int], None]
on_sethostname_return_t: Callable[['CPUState', int, int, int], None]
on_setitimer_enter_t: Callable[['CPUState', int, int, int, int], None]
on_setitimer_return_t: Callable[['CPUState', int, int, int, int], None]
on_setlogin_enter_t: Callable[['CPUState', int, int], None]
on_setlogin_return_t: Callable[['CPUState', int, int], None]
on_setloginclass_enter_t: Callable[['CPUState', int, int], None]
on_setloginclass_return_t: Callable[['CPUState', int, int], None]
on_setpgid_enter_t: Callable[['CPUState', int, int, int], None]
on_setpgid_return_t: Callable[['CPUState', int, int, int], None]
on_setpriority_enter_t: Callable[['CPUState', int, int, int, int], None]
on_setpriority_return_t: Callable[['CPUState', int, int, int, int], None]
on_setregid_enter_t: Callable[['CPUState', int, int, int], None]
on_setregid_return_t: Callable[['CPUState', int, int, int], None]
on_setresgid_enter_t: Callable[['CPUState', int, int, int, int], None]
on_setresgid_return_t: Callable[['CPUState', int, int, int, int], None]
on_setresuid_enter_t: Callable[['CPUState', int, int, int, int], None]
on_setresuid_return_t: Callable[['CPUState', int, int, int, int], None]
on_setreuid_enter_t: Callable[['CPUState', int, int, int], None]
on_setreuid_return_t: Callable[['CPUState', int, int, int], None]
on_setrlimit_enter_t: Callable[['CPUState', int, int, int], None]
on_setrlimit_return_t: Callable[['CPUState', int, int, int], None]
on_setsid_enter_t: Callable[['CPUState', int], None]
on_setsid_return_t: Callable[['CPUState', int], None]
on_setsockopt_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_setsockopt_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_settimeofday_enter_t: Callable[['CPUState', int, int, int], None]
on_settimeofday_return_t: Callable[['CPUState', int, int, int], None]
on_setuid_enter_t: Callable[['CPUState', int, int], None]
on_setuid_return_t: Callable[['CPUState', int, int], None]
on_shm_open2_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_shm_open2_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_shm_open_enter_t: Callable[['CPUState', int, int, int, int], None]
on_shm_open_return_t: Callable[['CPUState', int, int, int, int], None]
on_shm_rename_enter_t: Callable[['CPUState', int, int, int, int], None]
on_shm_rename_return_t: Callable[['CPUState', int, int, int, int], None]
on_shm_unlink_enter_t: Callable[['CPUState', int, int], None]
on_shm_unlink_return_t: Callable[['CPUState', int, int], None]
on_shmctl_enter_t: Callable[['CPUState', int, int, int, int], None]
on_shmctl_return_t: Callable[['CPUState', int, int, int, int], None]
on_shmdt_enter_t: Callable[['CPUState', int, int], None]
on_shmdt_return_t: Callable[['CPUState', int, int], None]
on_shmget_enter_t: Callable[['CPUState', int, int, int, int], None]
on_shmget_return_t: Callable[['CPUState', int, int, int, int], None]
on_shutdown_enter_t: Callable[['CPUState', int, int, int], None]
on_shutdown_return_t: Callable[['CPUState', int, int, int], None]
on_sigaction_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sigaction_return_t: Callable[['CPUState', int, int, int, int], None]
on_sigaltstack_enter_t: Callable[['CPUState', int, int, int], None]
on_sigaltstack_return_t: Callable[['CPUState', int, int, int], None]
on_sigblock_enter_t: Callable[['CPUState', int, int], None]
on_sigblock_return_t: Callable[['CPUState', int, int], None]
on_sigfastblock_enter_t: Callable[['CPUState', int, int, int], None]
on_sigfastblock_return_t: Callable[['CPUState', int, int, int], None]
on_sigpending_enter_t: Callable[['CPUState', int, int], None]
on_sigpending_return_t: Callable[['CPUState', int, int], None]
on_sigprocmask_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sigprocmask_return_t: Callable[['CPUState', int, int, int, int], None]
on_sigqueue_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sigqueue_return_t: Callable[['CPUState', int, int, int, int], None]
on_sigreturn_enter_t: Callable[['CPUState', int, int], None]
on_sigreturn_return_t: Callable[['CPUState', int, int], None]
on_sigsetmask_enter_t: Callable[['CPUState', int, int], None]
on_sigsetmask_return_t: Callable[['CPUState', int, int], None]
on_sigstack_enter_t: Callable[['CPUState', int, int, int], None]
on_sigstack_return_t: Callable[['CPUState', int, int, int], None]
on_sigsuspend_enter_t: Callable[['CPUState', int, int], None]
on_sigsuspend_return_t: Callable[['CPUState', int, int], None]
on_sigtimedwait_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sigtimedwait_return_t: Callable[['CPUState', int, int, int, int], None]
on_sigvec_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sigvec_return_t: Callable[['CPUState', int, int, int, int], None]
on_sigwait_enter_t: Callable[['CPUState', int, int, int], None]
on_sigwait_return_t: Callable[['CPUState', int, int, int], None]
on_sigwaitinfo_enter_t: Callable[['CPUState', int, int, int], None]
on_sigwaitinfo_return_t: Callable[['CPUState', int, int, int], None]
on_socket_enter_t: Callable[['CPUState', int, int, int, int], None]
on_socket_return_t: Callable[['CPUState', int, int, int, int], None]
on_socketpair_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_socketpair_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_ssm_t: Callable[['CPUState', int, int, int, int, bool, bool], None]
on_sstk_enter_t: Callable[['CPUState', int, int], None]
on_sstk_return_t: Callable[['CPUState', int, int], None]
on_stat_enter_t: Callable[['CPUState', int, int, int], None]
on_stat_return_t: Callable[['CPUState', int, int, int], None]
on_statfs_enter_t: Callable[['CPUState', int, int, int], None]
on_statfs_return_t: Callable[['CPUState', int, int, int], None]
on_swapcontext_enter_t: Callable[['CPUState', int, int, int], None]
on_swapcontext_return_t: Callable[['CPUState', int, int, int], None]
on_swapoff_enter_t: Callable[['CPUState', int, int], None]
on_swapoff_return_t: Callable[['CPUState', int, int], None]
on_swapon_enter_t: Callable[['CPUState', int, int], None]
on_swapon_return_t: Callable[['CPUState', int, int], None]
on_symlink_enter_t: Callable[['CPUState', int, int, int], None]
on_symlink_return_t: Callable[['CPUState', int, int, int], None]
on_symlinkat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_symlinkat_return_t: Callable[['CPUState', int, int, int, int], None]
on_sync_enter_t: Callable[['CPUState', int], None]
on_sync_return_t: Callable[['CPUState', int], None]
on_sys_accept4_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_accept4_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_accept_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_accept_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_access_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_access_return_t: Callable[['CPUState', int, int, int], None]
on_sys_acct_enter_t: Callable[['CPUState', int, int], None]
on_sys_acct_return_t: Callable[['CPUState', int, int], None]
on_sys_add_key_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_add_key_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_adjtimex_enter_t: Callable[['CPUState', int, int], None]
on_sys_adjtimex_return_t: Callable[['CPUState', int, int], None]
on_sys_alarm_enter_t: Callable[['CPUState', int, int], None]
on_sys_alarm_return_t: Callable[['CPUState', int, int], None]
on_sys_arch_prctl_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_arch_prctl_return_t: Callable[['CPUState', int, int, int], None]
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
on_sys_chmod_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_chmod_return_t: Callable[['CPUState', int, int, int], None]
on_sys_chown_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_chown_return_t: Callable[['CPUState', int, int, int, int], None]
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
on_sys_clone_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_clone_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_close_enter_t: Callable[['CPUState', int, int], None]
on_sys_close_return_t: Callable[['CPUState', int, int], None]
on_sys_connect_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_connect_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_copy_file_range_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_copy_file_range_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_creat_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_creat_return_t: Callable[['CPUState', int, int, int], None]
on_sys_delete_module_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_delete_module_return_t: Callable[['CPUState', int, int, int], None]
on_sys_dup2_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_dup2_return_t: Callable[['CPUState', int, int, int], None]
on_sys_dup3_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_dup3_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_dup_enter_t: Callable[['CPUState', int, int], None]
on_sys_dup_return_t: Callable[['CPUState', int, int], None]
on_sys_epoll_create1_enter_t: Callable[['CPUState', int, int], None]
on_sys_epoll_create1_return_t: Callable[['CPUState', int, int], None]
on_sys_epoll_create_enter_t: Callable[['CPUState', int, int], None]
on_sys_epoll_create_return_t: Callable[['CPUState', int, int], None]
on_sys_epoll_ctl_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_epoll_ctl_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_epoll_pwait_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_epoll_pwait_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_epoll_wait_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_epoll_wait_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_eventfd2_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_eventfd2_return_t: Callable[['CPUState', int, int, int], None]
on_sys_eventfd_enter_t: Callable[['CPUState', int, int], None]
on_sys_eventfd_return_t: Callable[['CPUState', int, int], None]
on_sys_execve_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_execve_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_execveat_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_execveat_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_exit_enter_t: Callable[['CPUState', int, int], None]
on_sys_exit_group_enter_t: Callable[['CPUState', int, int], None]
on_sys_exit_group_return_t: Callable[['CPUState', int, int], None]
on_sys_exit_return_t: Callable[['CPUState', int, int], None]
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
on_sys_fork_enter_t: Callable[['CPUState', int], None]
on_sys_fork_return_t: Callable[['CPUState', int], None]
on_sys_fremovexattr_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_fremovexattr_return_t: Callable[['CPUState', int, int, int], None]
on_sys_fsetxattr_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_fsetxattr_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_fstatfs_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_fstatfs_return_t: Callable[['CPUState', int, int, int], None]
on_sys_fsync_enter_t: Callable[['CPUState', int, int], None]
on_sys_fsync_return_t: Callable[['CPUState', int, int], None]
on_sys_ftruncate_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_ftruncate_return_t: Callable[['CPUState', int, int, int], None]
on_sys_futex_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_futex_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_sys_futimesat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_futimesat_return_t: Callable[['CPUState', int, int, int, int], None]
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
on_sys_getdents_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_getdents_return_t: Callable[['CPUState', int, int, int, int], None]
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
on_sys_getpgrp_enter_t: Callable[['CPUState', int], None]
on_sys_getpgrp_return_t: Callable[['CPUState', int], None]
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
on_sys_inotify_init_enter_t: Callable[['CPUState', int], None]
on_sys_inotify_init_return_t: Callable[['CPUState', int], None]
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
on_sys_ioperm_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_ioperm_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_iopl_enter_t: Callable[['CPUState', int, int], None]
on_sys_iopl_return_t: Callable[['CPUState', int, int], None]
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
on_sys_lchown_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_lchown_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_lgetxattr_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_lgetxattr_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_link_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_link_return_t: Callable[['CPUState', int, int, int], None]
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
on_sys_mkdir_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_mkdir_return_t: Callable[['CPUState', int, int, int], None]
on_sys_mkdirat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_mkdirat_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_mknod_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_mknod_return_t: Callable[['CPUState', int, int, int, int], None]
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
on_sys_modify_ldt_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_modify_ldt_return_t: Callable[['CPUState', int, int, int, int], None]
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
on_sys_newfstat_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_newfstat_return_t: Callable[['CPUState', int, int, int], None]
on_sys_newfstatat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_newfstatat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_newlstat_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_newlstat_return_t: Callable[['CPUState', int, int, int], None]
on_sys_newstat_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_newstat_return_t: Callable[['CPUState', int, int, int], None]
on_sys_newuname_enter_t: Callable[['CPUState', int, int], None]
on_sys_newuname_return_t: Callable[['CPUState', int, int], None]
on_sys_open_by_handle_at_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_open_by_handle_at_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_open_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_open_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_openat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_openat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_pause_enter_t: Callable[['CPUState', int], None]
on_sys_pause_return_t: Callable[['CPUState', int], None]
on_sys_perf_event_open_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_perf_event_open_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_personality_enter_t: Callable[['CPUState', int, int], None]
on_sys_personality_return_t: Callable[['CPUState', int, int], None]
on_sys_pipe2_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_pipe2_return_t: Callable[['CPUState', int, int, int], None]
on_sys_pipe_enter_t: Callable[['CPUState', int, int], None]
on_sys_pipe_return_t: Callable[['CPUState', int, int], None]
on_sys_pivot_root_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_pivot_root_return_t: Callable[['CPUState', int, int, int], None]
on_sys_pkey_alloc_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_pkey_alloc_return_t: Callable[['CPUState', int, int, int], None]
on_sys_pkey_free_enter_t: Callable[['CPUState', int, int], None]
on_sys_pkey_free_return_t: Callable[['CPUState', int, int], None]
on_sys_pkey_mprotect_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_pkey_mprotect_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_poll_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_poll_return_t: Callable[['CPUState', int, int, int, int], None]
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
on_sys_readlink_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_readlink_return_t: Callable[['CPUState', int, int, int, int], None]
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
on_sys_rename_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_rename_return_t: Callable[['CPUState', int, int, int], None]
on_sys_renameat2_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_renameat2_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_renameat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_renameat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_request_key_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_request_key_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_restart_syscall_enter_t: Callable[['CPUState', int], None]
on_sys_restart_syscall_return_t: Callable[['CPUState', int], None]
on_sys_rmdir_enter_t: Callable[['CPUState', int, int], None]
on_sys_rmdir_return_t: Callable[['CPUState', int, int], None]
on_sys_rt_sigaction_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_rt_sigaction_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_rt_sigpending_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_rt_sigpending_return_t: Callable[['CPUState', int, int, int], None]
on_sys_rt_sigprocmask_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_rt_sigprocmask_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_rt_sigqueueinfo_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_rt_sigqueueinfo_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_rt_sigreturn_enter_t: Callable[['CPUState', int], None]
on_sys_rt_sigreturn_return_t: Callable[['CPUState', int], None]
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
on_sys_select_enter_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_select_return_t: Callable[['CPUState', int, int, int, int, int, int], None]
on_sys_semctl_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_semctl_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_semget_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_semget_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_semop_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_semop_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_semtimedop_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_semtimedop_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_sendfile64_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_sendfile64_return_t: Callable[['CPUState', int, int, int, int, int], None]
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
on_sys_signalfd_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_signalfd_return_t: Callable[['CPUState', int, int, int, int], None]
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
on_sys_symlink_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_symlink_return_t: Callable[['CPUState', int, int, int], None]
on_sys_symlinkat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_symlinkat_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_sync_enter_t: Callable[['CPUState', int], None]
on_sys_sync_file_range_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_sync_file_range_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_sync_return_t: Callable[['CPUState', int], None]
on_sys_syncfs_enter_t: Callable[['CPUState', int, int], None]
on_sys_syncfs_return_t: Callable[['CPUState', int, int], None]
on_sys_sysctl_enter_t: Callable[['CPUState', int, int], None]
on_sys_sysctl_return_t: Callable[['CPUState', int, int], None]
on_sys_sysfs_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_sysfs_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_sysinfo_enter_t: Callable[['CPUState', int, int], None]
on_sys_sysinfo_return_t: Callable[['CPUState', int, int], None]
on_sys_syslog_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_syslog_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_tee_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_tee_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_tgkill_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_tgkill_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_time_enter_t: Callable[['CPUState', int, int], None]
on_sys_time_return_t: Callable[['CPUState', int, int], None]
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
on_sys_umount_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_umount_return_t: Callable[['CPUState', int, int, int], None]
on_sys_unlink_enter_t: Callable[['CPUState', int, int], None]
on_sys_unlink_return_t: Callable[['CPUState', int, int], None]
on_sys_unlinkat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_sys_unlinkat_return_t: Callable[['CPUState', int, int, int, int], None]
on_sys_unshare_enter_t: Callable[['CPUState', int, int], None]
on_sys_unshare_return_t: Callable[['CPUState', int, int], None]
on_sys_userfaultfd_enter_t: Callable[['CPUState', int, int], None]
on_sys_userfaultfd_return_t: Callable[['CPUState', int, int], None]
on_sys_ustat_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_ustat_return_t: Callable[['CPUState', int, int, int], None]
on_sys_utime_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_utime_return_t: Callable[['CPUState', int, int, int], None]
on_sys_utimensat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_utimensat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_sys_utimes_enter_t: Callable[['CPUState', int, int, int], None]
on_sys_utimes_return_t: Callable[['CPUState', int, int, int], None]
on_sys_vfork_enter_t: Callable[['CPUState', int], None]
on_sys_vfork_return_t: Callable[['CPUState', int], None]
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
on_sysarch_enter_t: Callable[['CPUState', int, int, int], None]
on_sysarch_return_t: Callable[['CPUState', int, int, int], None]
on_taint_change_t: Callable[['addr_struct', int], None]
on_taint_prop_t: Callable[['addr_struct', 'addr_struct', int], None]
on_task_change_t: Callable[['CPUState'], None]
on_thr_create_enter_t: Callable[['CPUState', int, int, int, int], None]
on_thr_create_return_t: Callable[['CPUState', int, int, int, int], None]
on_thr_exit_enter_t: Callable[['CPUState', int, int], None]
on_thr_exit_return_t: Callable[['CPUState', int, int], None]
on_thr_kill2_enter_t: Callable[['CPUState', int, int, int, int], None]
on_thr_kill2_return_t: Callable[['CPUState', int, int, int, int], None]
on_thr_kill_enter_t: Callable[['CPUState', int, int, int], None]
on_thr_kill_return_t: Callable[['CPUState', int, int, int], None]
on_thr_new_enter_t: Callable[['CPUState', int, int, int], None]
on_thr_new_return_t: Callable[['CPUState', int, int, int], None]
on_thr_self_enter_t: Callable[['CPUState', int, int], None]
on_thr_self_return_t: Callable[['CPUState', int, int], None]
on_thr_set_name_enter_t: Callable[['CPUState', int, int, int], None]
on_thr_set_name_return_t: Callable[['CPUState', int, int, int], None]
on_thr_suspend_enter_t: Callable[['CPUState', int, int], None]
on_thr_suspend_return_t: Callable[['CPUState', int, int], None]
on_thr_wake_enter_t: Callable[['CPUState', int, int], None]
on_thr_wake_return_t: Callable[['CPUState', int, int], None]
on_thread_end_t: Callable[['CPUState', bytes, int, int, int], None]
on_thread_start_t: Callable[['CPUState', bytes, int, int, int], None]
on_truncate_enter_t: Callable[['CPUState', int, int, int], None]
on_truncate_return_t: Callable[['CPUState', int, int, int], None]
on_umask_enter_t: Callable[['CPUState', int, int], None]
on_umask_return_t: Callable[['CPUState', int, int], None]
on_uname_enter_t: Callable[['CPUState', int, int], None]
on_uname_return_t: Callable[['CPUState', int, int], None]
on_undelete_enter_t: Callable[['CPUState', int, int], None]
on_undelete_return_t: Callable[['CPUState', int, int], None]
on_unknown_sys_enter_t: Callable[['CPUState', int, int], None]
on_unknown_sys_return_t: Callable[['CPUState', int, int], None]
on_unlink_enter_t: Callable[['CPUState', int, int], None]
on_unlink_return_t: Callable[['CPUState', int, int], None]
on_unlinkat_enter_t: Callable[['CPUState', int, int, int, int], None]
on_unlinkat_return_t: Callable[['CPUState', int, int, int, int], None]
on_unmount_enter_t: Callable[['CPUState', int, int, int], None]
on_unmount_return_t: Callable[['CPUState', int, int, int], None]
on_utimensat_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_utimensat_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_utimes_enter_t: Callable[['CPUState', int, int, int], None]
on_utimes_return_t: Callable[['CPUState', int, int, int], None]
on_utrace_enter_t: Callable[['CPUState', int, int, int], None]
on_utrace_return_t: Callable[['CPUState', int, int, int], None]
on_uuidgen_enter_t: Callable[['CPUState', int, int, int], None]
on_uuidgen_return_t: Callable[['CPUState', int, int, int], None]
on_vadvise_enter_t: Callable[['CPUState', int, int], None]
on_vadvise_return_t: Callable[['CPUState', int, int], None]
on_vfork_enter_t: Callable[['CPUState', int], None]
on_vfork_return_t: Callable[['CPUState', int], None]
on_wait4_enter_t: Callable[['CPUState', int, int, int, int, int], None]
on_wait4_return_t: Callable[['CPUState', int, int, int, int, int], None]
on_wait6_enter_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_wait6_return_t: Callable[['CPUState', int, int, int, int, int, int, int], None]
on_wait_enter_t: Callable[['CPUState', int], None]
on_wait_return_t: Callable[['CPUState', int], None]
on_write_enter_t: Callable[['CPUState', int, int, int, int], None]
on_write_return_t: Callable[['CPUState', int, int, int, int], None]
on_writev_enter_t: Callable[['CPUState', int, int, int, int], None]
on_writev_return_t: Callable[['CPUState', int, int, int, int], None]
on_yield_enter_t: Callable[['CPUState', int], None]
on_yield_return_t: Callable[['CPUState', int], None]
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

