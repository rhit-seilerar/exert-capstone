from enum import IntEnum
from collections.abc import Callable
import ctypes

class AccelState:
    parent_obj: Object

class Addr:
    typ: AddrType
    val: ctypes.c_ulong
    off: ctypes.c_ushort
    flag: AddrFlag

class AddrFlag(IntEnum):
    FUNCARG: int = 3
    READLOG: int = 2
    EXCEPTION: int = 1
    IRRELEVANT: int = 5

class AddrRange:
    start: ctypes.Array[ctypes.c_ubyte]
    size: ctypes.Array[ctypes.c_ubyte]

class AddrType(IntEnum):
    ADDR_LAST: int = 10
    RET: int = 9
    CONST: int = 8
    UNK: int = 7
    GSPEC: int = 6
    GREG: int = 5
    LADDR: int = 4
    PADDR: int = 3
    IADDR: int = 2
    MADDR: int = 1
    HADDR: int = 0

class AddressSpace:
    rcu: rcu_head
    name: ctypes._Pointer[ctypes.c_char]
    root: ctypes._Pointer[MemoryRegion]
    ref_count: ctypes.c_int
    malloced: ctypes.c_bool
    current_map: ctypes._Pointer[FlatView]
    ioeventfd_nb: ctypes.c_int
    ioeventfds: ctypes._Pointer[MemoryRegionIoeventfd]
    dispatch: ctypes._Pointer[AddressSpaceDispatch]
    next_dispatch: ctypes._Pointer[AddressSpaceDispatch]
    dispatch_listener: MemoryListener
    listeners: memory_listeners_as
    class internal_7:
        tqe_next: ctypes._Pointer[AddressSpace]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[AddressSpace]]

    address_spaces_link: internal_7

class BNDCSReg:
    cfgu: ctypes.c_ulong
    sts: ctypes.c_ulong

class BNDReg:
    lb: ctypes.c_ulong
    ub: ctypes.c_ulong

BlockCompletionFunc: None
class BusState:
    obj: Object
    parent: ctypes._Pointer[DeviceState]
    name: ctypes._Pointer[ctypes.c_char]
    hotplug_handler: ctypes._Pointer[HotplugHandler]
    max_index: ctypes.c_int
    realized: ctypes.c_bool
    children: ChildrenHead
    class internal_21:
        le_next: ctypes._Pointer[BusState]
        le_prev: ctypes._Pointer[ctypes._Pointer[BusState]]

    sibling: internal_21

class CPUAddressSpace:
    cpu: ctypes._Pointer[CPUState]
    memory_dispatch: ctypes._Pointer[AddressSpaceDispatch]
    tcg_as_listener: MemoryListener
setattr(CPUAddressSpace, "as", ctypes._Pointer[AddressSpace]())

CPUArchIdList: ctypes.c_ulong
class CPUBreakpoint:
    pc: ctypes.c_ulong
    rr_instr_count: ctypes.c_ulong
    flags: ctypes.c_int
    entry: CPUBreakpoint_qtailq

class CPUBreakpoint_qtailq:
    tqe_next: ctypes._Pointer[CPUBreakpoint]
    tqe_prev: ctypes._Pointer[ctypes._Pointer[CPUBreakpoint]]

class CPUIOTLBEntry:
    addr: ctypes.c_ulong
    attrs: MemTxAttrs

CPUReadMemoryFunc: ctypes.c_uint
class CPUState:
    parent_obj: DeviceState
    nr_cores: ctypes.c_int
    nr_threads: ctypes.c_int
    numa_node: ctypes.c_int
    thread: ctypes._Pointer[QemuThread]
    thread_id: ctypes.c_int
    host_tid: ctypes.c_uint
    running: ctypes.c_bool
    has_waiter: ctypes.c_bool
    halt_cond: ctypes._Pointer[QemuCond]
    thread_kicked: ctypes.c_bool
    created: ctypes.c_bool
    stop: ctypes.c_bool
    stopped: ctypes.c_bool
    unplug: ctypes.c_bool
    crash_occurred: ctypes.c_bool
    exit_request: ctypes.c_bool
    interrupt_request: ctypes.c_uint
    singlestep_enabled: ctypes.c_int
    icount_budget: ctypes.c_long
    icount_extra: ctypes.c_long
    jmp_env: ctypes.Array[ctypes.c_ubyte]
    work_mutex: QemuMutex
    queued_work_first: ctypes._Pointer[qemu_work_item]
    queued_work_last: ctypes._Pointer[qemu_work_item]
    cpu_ases: ctypes._Pointer[CPUAddressSpace]
    num_ases: ctypes.c_int
    memory: ctypes._Pointer[MemoryRegion]
    env_ptr: ctypes._Pointer[CPUX86State]
    tb_jmp_cache: ctypes.Array[ctypes._Pointer[TranslationBlock]]
    gdb_regs: ctypes._Pointer[GDBRegisterState]
    gdb_num_regs: ctypes.c_int
    gdb_num_g_regs: ctypes.c_int
    class internal_23:
        tqe_next: ctypes._Pointer[CPUState]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[CPUState]]

    node: internal_23
    breakpoints: breakpoints_head
    watchpoints: watchpoints_head
    watchpoint_hit: ctypes._Pointer[CPUWatchpoint]
    watchpoints_disabled: ctypes.c_bool
    opaque: ctypes.c_void_p
    mem_io_pc: ctypes.c_ulong
    mem_io_vaddr: ctypes.c_ulong
    kvm_fd: ctypes.c_int
    kvm_vcpu_dirty: ctypes.c_bool
    kvm_state: ctypes._Pointer[KVMState]
    kvm_run: ctypes._Pointer[kvm_run]
    trace_dstate: ctypes._Pointer[ctypes.c_ulong]
    cpu_index: ctypes.c_int
    halted: ctypes.c_uint
    class internal_24:
        u32: ctypes.c_uint
        u16: icount_decr_u16

    icount_decr: internal_24
    can_do_io: ctypes.c_uint
    exception_index: ctypes.c_int
    rr_guest_instr_count: ctypes.c_ulong
    panda_guest_pc: ctypes.c_ulong
    reverse_flags: ctypes.c_ubyte
    last_gdb_instr: ctypes.c_ulong
    last_bp_hit_instr: ctypes.c_ulong
    temp_rr_bp_instr: ctypes.c_ulong
    throttle_thread_scheduled: ctypes.c_bool
    tcg_exit_req: ctypes.c_uint
    hax_vcpu_dirty: ctypes.c_bool
    hax_vcpu: ctypes._Pointer[hax_vcpu_state]
    pending_tlb_flush: ctypes.c_ushort
setattr(CPUState, "as", ctypes._Pointer[AddressSpace]())

class CPUTLBEntry:
    addr_read: ctypes.c_uint
    addr_write: ctypes.c_uint
    addr_code: ctypes.c_uint
    addend: ctypes.c_ulong
    dummy: ctypes.Array[ctypes.c_ubyte]

class CPUWatchpoint:
    virtaddr: ctypes.c_ulong
    len: ctypes.c_ulong
    hitaddr: ctypes.c_ulong
    hitattrs: MemTxAttrs
    flags: ctypes.c_int
    class internal_6:
        tqe_next: ctypes._Pointer[CPUWatchpoint]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[CPUWatchpoint]]

    entry: internal_6

CPUWriteMemoryFunc: None
class CPUX86State:
    regs: ctypes.Array[ctypes.c_uint]
    eip: ctypes.c_uint
    eflags: ctypes.c_uint
    cc_dst: ctypes.c_uint
    cc_src: ctypes.c_uint
    cc_src2: ctypes.c_uint
    cc_op: ctypes.c_uint
    df: ctypes.c_int
    hflags: ctypes.c_uint
    hflags2: ctypes.c_uint
    segs: ctypes.Array[SegmentCache]
    ldt: SegmentCache
    tr: SegmentCache
    gdt: SegmentCache
    idt: SegmentCache
    cr: ctypes.Array[ctypes.c_uint]
    a20_mask: ctypes.c_int
    bnd_regs: ctypes.Array[BNDReg]
    bndcs_regs: BNDCSReg
    msr_bndcfgs: ctypes.c_ulong
    efer: ctypes.c_ulong
    fpstt: ctypes.c_uint
    fpus: ctypes.c_ushort
    fpuc: ctypes.c_ushort
    fptags: ctypes.Array[ctypes.c_ubyte]
    fpregs: ctypes.Array[ctypes.Array[ctypes.c_ubyte]]
    fpop: ctypes.c_ushort
    fpip: ctypes.c_ulong
    fpdp: ctypes.c_ulong
    fp_status: float_status
    ft0: floatx80
    mmx_status: float_status
    sse_status: float_status
    mxcsr: ctypes.c_uint
    xmm_regs: ctypes.Array[ctypes.Array[ctypes.c_ubyte]]
    xmm_t0: ctypes.Array[ctypes.c_ubyte]
    mmx_t0: ctypes.Array[ctypes.c_ubyte]
    opmask_regs: ctypes.Array[ctypes.c_ulong]
    sysenter_cs: ctypes.c_uint
    sysenter_esp: ctypes.c_uint
    sysenter_eip: ctypes.c_uint
    star: ctypes.c_ulong
    vm_hsave: ctypes.c_ulong
    tsc: ctypes.c_ulong
    tsc_adjust: ctypes.c_ulong
    tsc_deadline: ctypes.c_ulong
    tsc_aux: ctypes.c_ulong
    xcr0: ctypes.c_ulong
    mcg_status: ctypes.c_ulong
    msr_ia32_misc_enable: ctypes.c_ulong
    msr_ia32_feature_control: ctypes.c_ulong
    msr_fixed_ctr_ctrl: ctypes.c_ulong
    msr_global_ctrl: ctypes.c_ulong
    msr_global_status: ctypes.c_ulong
    msr_global_ovf_ctrl: ctypes.c_ulong
    msr_fixed_counters: ctypes.Array[ctypes.c_ulong]
    msr_gp_counters: ctypes.Array[ctypes.c_ulong]
    msr_gp_evtsel: ctypes.Array[ctypes.c_ulong]
    pat: ctypes.c_ulong
    smbase: ctypes.c_uint
    pkru: ctypes.c_uint
    system_time_msr: ctypes.c_ulong
    wall_clock_msr: ctypes.c_ulong
    steal_time_msr: ctypes.c_ulong
    async_pf_en_msr: ctypes.c_ulong
    pv_eoi_en_msr: ctypes.c_ulong
    msr_hv_hypercall: ctypes.c_ulong
    msr_hv_guest_os_id: ctypes.c_ulong
    msr_hv_vapic: ctypes.c_ulong
    msr_hv_tsc: ctypes.c_ulong
    msr_hv_crash_params: ctypes.Array[ctypes.c_ulong]
    msr_hv_runtime: ctypes.c_ulong
    msr_hv_synic_control: ctypes.c_ulong
    msr_hv_synic_version: ctypes.c_ulong
    msr_hv_synic_evt_page: ctypes.c_ulong
    msr_hv_synic_msg_page: ctypes.c_ulong
    msr_hv_synic_sint: ctypes.Array[ctypes.c_ulong]
    msr_hv_stimer_config: ctypes.Array[ctypes.c_ulong]
    msr_hv_stimer_count: ctypes.Array[ctypes.c_ulong]
    error_code: ctypes.c_int
    exception_is_int: ctypes.c_int
    exception_next_eip: ctypes.c_uint
    dr: ctypes.Array[ctypes.c_uint]
    cpu_breakpoint: ctypes.Array[ctypes._Pointer[CPUBreakpoint]]
    cpu_watchpoint: ctypes.Array[ctypes._Pointer[CPUWatchpoint]]
    old_exception: ctypes.c_int
    vm_vmcb: ctypes.c_ulong
    tsc_offset: ctypes.c_ulong
    intercept: ctypes.c_ulong
    intercept_cr_read: ctypes.c_ushort
    intercept_cr_write: ctypes.c_ushort
    intercept_dr_read: ctypes.c_ushort
    intercept_dr_write: ctypes.c_ushort
    intercept_exceptions: ctypes.c_uint
    v_tpr: ctypes.c_ubyte
    nmi_injected: ctypes.c_ubyte
    nmi_pending: ctypes.c_ubyte
    tlb_table: ctypes.Array[ctypes.Array[CPUTLBEntry]]
    tlb_v_table: ctypes.Array[ctypes.Array[CPUTLBEntry]]
    iotlb: ctypes.Array[ctypes.Array[CPUIOTLBEntry]]
    iotlb_v: ctypes.Array[ctypes.Array[CPUIOTLBEntry]]
    tlb_flush_addr: ctypes.c_uint
    tlb_flush_mask: ctypes.c_uint
    vtlb_index: ctypes.c_uint
    cpuid_min_level: ctypes.c_uint
    cpuid_min_xlevel: ctypes.c_uint
    cpuid_min_xlevel2: ctypes.c_uint
    cpuid_max_level: ctypes.c_uint
    cpuid_max_xlevel: ctypes.c_uint
    cpuid_max_xlevel2: ctypes.c_uint
    cpuid_level: ctypes.c_uint
    cpuid_xlevel: ctypes.c_uint
    cpuid_xlevel2: ctypes.c_uint
    cpuid_vendor1: ctypes.c_uint
    cpuid_vendor2: ctypes.c_uint
    cpuid_vendor3: ctypes.c_uint
    cpuid_version: ctypes.c_uint
    features: ctypes.Array[ctypes.c_uint]
    user_features: ctypes.Array[ctypes.c_uint]
    cpuid_model: ctypes.Array[ctypes.c_uint]
    mtrr_fixed: ctypes.Array[ctypes.c_ulong]
    mtrr_deftype: ctypes.c_ulong
    mtrr_var: ctypes.Array[MTRRVar]
    mp_state: ctypes.c_uint
    exception_injected: ctypes.c_int
    interrupt_injected: ctypes.c_int
    soft_interrupt: ctypes.c_ubyte
    has_error_code: ctypes.c_ubyte
    sipi_vector: ctypes.c_uint
    tsc_valid: ctypes.c_bool
    tsc_khz: ctypes.c_long
    user_tsc_khz: ctypes.c_long
    kvm_xsave_buf: ctypes.c_void_p
    mcg_cap: ctypes.c_ulong
    mcg_ctl: ctypes.c_ulong
    mcg_ext_ctl: ctypes.c_ulong
    mce_banks: ctypes.Array[ctypes.c_ulong]
    xstate_bv: ctypes.c_ulong
    fpus_vmstate: ctypes.c_ushort
    fptag_vmstate: ctypes.c_ushort
    fpregs_format_vmstate: ctypes.c_ushort
    xss: ctypes.c_ulong
    tpr_access_type: TPRAccess

class CharBackend:
    chr: ctypes._Pointer[Chardev]
    chr_event: Callable[[ctypes.c_void_p, ctypes.c_int], None]
    chr_can_read: Callable[[ctypes.c_void_p], ctypes.c_int]
    chr_read: Callable[[ctypes.c_void_p, ctypes._Pointer[ctypes.c_ubyte], ctypes.c_int], None]
    opaque: ctypes.c_void_p
    tag: ctypes.c_int
    fe_open: ctypes.c_int

class Chardev:
    parent_obj: Object
    chr_write_lock: QemuMutex
    be: ctypes._Pointer[CharBackend]
    label: ctypes._Pointer[ctypes.c_char]
    filename: ctypes._Pointer[ctypes.c_char]
    logfd: ctypes.c_int
    be_open: ctypes.c_int
    fd_in_tag: ctypes.c_uint
    features: ctypes.Array[ctypes.c_ulong]
    class internal_18:
        tqe_next: ctypes._Pointer[Chardev]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[Chardev]]

    next: internal_18

class ChildrenHead:
    tqh_first: ctypes._Pointer[BusChild]
    tqh_last: ctypes._Pointer[ctypes._Pointer[BusChild]]

Const: ctypes.c_ulong
class CosiFile:
    addr: ctypes.c_uint
    file_struct: File
    name: ctypes._Pointer[String]
    fd: ctypes.c_uint

class CosiFiles:
    pass

class CosiMappings:
    modules: ctypes._Pointer[Vec_CosiModule]

class CosiModule:
    modd: ctypes.c_uint
    base: ctypes.c_uint
    size: ctypes.c_uint
    vma: VmAreaStruct
    file: ctypes._Pointer[String]
    name: ctypes._Pointer[String]

class CosiProc:
    addr: ctypes.c_uint
    task: TaskStruct
    name: ctypes._Pointer[String]
    ppid: ctypes.c_uint
    mm: ctypes._Pointer[MmStruct]
    asid: ctypes.c_uint
    taskd: ctypes.c_uint

class CosiThread:
    tid: ctypes.c_uint
    pid: ctypes.c_uint

class DeviceState:
    parent_obj: Object
    id: ctypes._Pointer[ctypes.c_char]
    realized: ctypes.c_bool
    pending_deleted_event: ctypes.c_bool
    opts: ctypes._Pointer[QemuOpts]
    hotplugged: ctypes.c_int
    parent_bus: ctypes._Pointer[BusState]
    class internal_16:
        lh_first: ctypes._Pointer[NamedGPIOList]

    gpios: internal_16
    class internal_17:
        lh_first: ctypes._Pointer[BusState]

    child_bus: internal_17
    num_child_bus: ctypes.c_int
    instance_id_alias: ctypes.c_int
    alias_required_for_version: ctypes.c_int

class EventNotifier:
    rfd: ctypes.c_int
    wfd: ctypes.c_int

class FILE:
    pass

FPReg: ctypes.Array[ctypes.c_ubyte]
FeatureWordArray: ctypes.Array[ctypes.c_uint]
class File:
    f_path: Path
    f_pos: ctypes.c_uint

GArray: None
class GDBRegisterState:
    base_reg: ctypes.c_int
    num_regs: ctypes.c_int
    get_reg: ctypes.c_int
    set_reg: ctypes.c_int
    xml: ctypes._Pointer[ctypes.c_char]
    next: ctypes._Pointer[GDBRegisterState]

class GHashTable:
    pass

GReg: ctypes.c_ulong
GSpec: ctypes.c_ulong
HAddr: ctypes.c_ulong
class HotplugHandler:
    Parent: Object

IAddr: ctypes.c_ulong
IOCanReadHandler: ctypes.c_int
IOEventHandler: None
class IOMMUAccessFlags(IntEnum):
    IOMMU_RW: int = 3
    IOMMU_WO: int = 2
    IOMMU_RO: int = 1
    IOMMU_NONE: int = 0

class IOMMUNotifierFlag(IntEnum):
    IOMMU_NOTIFIER_MAP: int = 2
    IOMMU_NOTIFIER_UNMAP: int = 1
    IOMMU_NOTIFIER_NONE: int = 0

class IOMMUTLBEntry:
    target_as: ctypes._Pointer[AddressSpace]
    iova: ctypes.c_ulong
    translated_addr: ctypes.c_ulong
    addr_mask: ctypes.c_ulong
    perm: IOMMUAccessFlags

IOReadHandler: None
class InsnFlag(IntEnum):
    INSNREADLOG: int = 1

Int128: ctypes.Array[ctypes.c_ubyte]
LAddr: ctypes.c_ulong
class ListHead:
    next: ctypes.c_uint
    prev: ctypes.c_uint

class Location:
    num: ctypes.c_int
    ptr: ctypes.c_void_p
    prev: ctypes._Pointer[Location]

MAddr: ctypes.c_ulong
MMXReg: ctypes.Array[ctypes.c_ubyte]
class MTRRVar:
    base: ctypes.c_ulong
    mask: ctypes.c_ulong

class MachineState:
    parent_obj: Object
    sysbus_notifier: Notifier
    accel: ctypes._Pointer[ctypes.c_char]
    kernel_irqchip_allowed: ctypes.c_bool
    kernel_irqchip_required: ctypes.c_bool
    kernel_irqchip_split: ctypes.c_bool
    kvm_shadow_mem: ctypes.c_int
    dtb: ctypes._Pointer[ctypes.c_char]
    dumpdtb: ctypes._Pointer[ctypes.c_char]
    phandle_start: ctypes.c_int
    dt_compatible: ctypes._Pointer[ctypes.c_char]
    dump_guest_core: ctypes.c_bool
    mem_merge: ctypes.c_bool
    usb: ctypes.c_bool
    usb_disabled: ctypes.c_bool
    igd_gfx_passthru: ctypes.c_bool
    firmware: ctypes._Pointer[ctypes.c_char]
    iommu: ctypes.c_bool
    suppress_vmdesc: ctypes.c_bool
    enforce_config_section: ctypes.c_bool
    enable_graphics: ctypes.c_bool
    board_id: ctypes.c_int
    mem_map_str: ctypes._Pointer[ctypes.c_char]
    ram_size: ctypes.c_ulong
    maxram_size: ctypes.c_ulong
    ram_slots: ctypes.c_ulong
    boot_order: ctypes._Pointer[ctypes.c_char]
    kernel_filename: ctypes._Pointer[ctypes.c_char]
    kernel_cmdline: ctypes._Pointer[ctypes.c_char]
    initrd_filename: ctypes._Pointer[ctypes.c_char]
    cpu_model: ctypes._Pointer[ctypes.c_char]
    accelerator: ctypes._Pointer[AccelState]
    possible_cpus: ctypes._Pointer[ctypes.c_ulong]

class MemTxAttrs:
    unspecified: ctypes.c_uint
    secure: ctypes.c_uint
    user: ctypes.c_uint
    requester_id: ctypes.c_uint

MemTxResult: ctypes.c_ulong
class MemoryListener:
    begin: Callable[[ctypes._Pointer[MemoryListener]], None]
    commit: Callable[[ctypes._Pointer[MemoryListener]], None]
    region_add: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection]], None]
    region_del: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection]], None]
    region_nop: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection]], None]
    log_start: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection], ctypes.c_int, ctypes.c_int], None]
    log_stop: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection], ctypes.c_int, ctypes.c_int], None]
    log_sync: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection]], None]
    log_global_start: Callable[[ctypes._Pointer[MemoryListener]], None]
    log_global_stop: Callable[[ctypes._Pointer[MemoryListener]], None]
    eventfd_add: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection], ctypes.c_bool, ctypes.c_ulong, ctypes._Pointer[EventNotifier]], None]
    eventfd_del: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection], ctypes.c_bool, ctypes.c_ulong, ctypes._Pointer[EventNotifier]], None]
    coalesced_mmio_add: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection], ctypes.c_ulong, ctypes.c_ulong], None]
    coalesced_mmio_del: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection], ctypes.c_ulong, ctypes.c_ulong], None]
    priority: ctypes.c_uint
    address_space: ctypes._Pointer[AddressSpace]
    class internal_13:
        tqe_next: ctypes._Pointer[MemoryListener]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[MemoryListener]]

    link: internal_13
    class internal_14:
        tqe_next: ctypes._Pointer[MemoryListener]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[MemoryListener]]

    link_as: internal_14

class MemoryRegion:
    parent_obj: Object
    romd_mode: ctypes.c_bool
    ram: ctypes.c_bool
    subpage: ctypes.c_bool
    readonly: ctypes.c_bool
    rom_device: ctypes.c_bool
    flush_coalesced_mmio: ctypes.c_bool
    global_locking: ctypes.c_bool
    dirty_log_mask: ctypes.c_ubyte
    ram_block: ctypes._Pointer[RAMBlock]
    owner: ctypes._Pointer[Object]
    iommu_ops: ctypes._Pointer[MemoryRegionIOMMUOps]
    ops: ctypes._Pointer[MemoryRegionOps]
    opaque: ctypes.c_void_p
    container: ctypes._Pointer[MemoryRegion]
    size: ctypes.Array[ctypes.c_ubyte]
    addr: ctypes.c_ulong
    destructor: Callable[[ctypes._Pointer[MemoryRegion]], None]
    align: ctypes.c_ulong
    terminates: ctypes.c_bool
    ram_device: ctypes.c_bool
    enabled: ctypes.c_bool
    warning_printed: ctypes.c_bool
    vga_logging_count: ctypes.c_ubyte
    alias: ctypes._Pointer[MemoryRegion]
    alias_offset: ctypes.c_ulong
    priority: ctypes.c_int
    subregions: subregions
    class internal_11:
        tqe_next: ctypes._Pointer[MemoryRegion]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[MemoryRegion]]

    subregions_link: internal_11
    coalesced: coalesced_ranges
    name: ctypes._Pointer[ctypes.c_char]
    ioeventfd_nb: ctypes.c_uint
    ioeventfds: ctypes._Pointer[MemoryRegionIoeventfd]
    class internal_12:
        lh_first: ctypes._Pointer[IOMMUNotifier]

    iommu_notify: internal_12
    iommu_notify_flags: IOMMUNotifierFlag

class MemoryRegionIOMMUOps:
    translate: Callable[[ctypes._Pointer[MemoryRegion], ctypes.c_ulong, ctypes.c_bool], IOMMUTLBEntry]
    get_min_page_size: Callable[[ctypes._Pointer[MemoryRegion]], ctypes.c_ulong]
    notify_flag_changed: Callable[[ctypes._Pointer[MemoryRegion], IOMMUNotifierFlag, IOMMUNotifierFlag], None]

class MemoryRegionIoeventfd:
    addr: AddrRange
    match_data: ctypes.c_bool
    data: ctypes.c_ulong
    e: ctypes._Pointer[EventNotifier]

class MemoryRegionMmio:
    read: ctypes.Array[Callable[[ctypes.c_void_p, ctypes.c_ulong], ctypes.c_uint]]
    write: ctypes.Array[Callable[[ctypes.c_void_p, ctypes.c_ulong, ctypes.c_uint], None]]

class MemoryRegionOps:
    read: Callable[[ctypes.c_void_p, ctypes.c_ulong, ctypes.c_uint], ctypes.c_ulong]
    write: Callable[[ctypes.c_void_p, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_uint], None]
    read_with_attrs: Callable[[ctypes.c_void_p, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ulong], ctypes.c_uint, MemTxAttrs], ctypes.c_ulong]
    write_with_attrs: Callable[[ctypes.c_void_p, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_uint, MemTxAttrs], ctypes.c_ulong]
    endianness: device_endian
    class internal_9:
        min_access_size: ctypes.c_uint
        max_access_size: ctypes.c_uint
        unaligned: ctypes.c_bool
        accepts: Callable[[ctypes.c_void_p, ctypes.c_ulong, ctypes.c_uint, ctypes.c_bool], ctypes.c_bool]

    valid: internal_9
    class internal_10:
        min_access_size: ctypes.c_uint
        max_access_size: ctypes.c_uint
        unaligned: ctypes.c_bool

    impl: internal_10
    old_mmio: MemoryRegionMmio

class MemoryRegionSection:
    mr: ctypes._Pointer[MemoryRegion]
    address_space: ctypes._Pointer[AddressSpace]
    offset_within_region: ctypes.c_ulong
    size: ctypes.Array[ctypes.c_ubyte]
    offset_within_address_space: ctypes.c_ulong
    readonly: ctypes.c_bool

class MmStruct:
    pgd: ctypes.c_uint
    arg_start: ctypes.c_uint
    start_brk: ctypes.c_uint
    brk: ctypes.c_uint
    start_stack: ctypes.c_uint
    mmap: ctypes.c_uint

class Monitor:
    chr: CharBackend
    reset_seen: ctypes.c_int
    flags: ctypes.c_int
    suspend_cnt: ctypes.c_int
    skip_flush: ctypes.c_bool
    out_lock: QemuMutex
    outbuf: ctypes._Pointer[QString]
    out_watch: ctypes.c_uint
    mux_out: ctypes.c_int
    rs: ctypes._Pointer[ReadLineState]
    qmp: ctypes.Array[ctypes.c_ubyte]
    mon_cpu: ctypes._Pointer[CPUState]
    password_completion_cb: Callable[[ctypes.c_void_p, ctypes.c_int], None]
    password_opaque: ctypes.c_void_p
    cmd_table: ctypes._Pointer[ctypes.Array[ctypes.c_ubyte]]
    class internal_19:
        lh_first: ctypes._Pointer[mon_fd_t]

    fds: internal_19
    class internal_20:
        le_next: ctypes._Pointer[Monitor]
        le_prev: ctypes._Pointer[ctypes._Pointer[Monitor]]

    entry: internal_20

MonitorQMP: ctypes.Array[ctypes.c_ubyte]
class Notifier:
    notify: Callable[[ctypes._Pointer[Notifier], ctypes.c_void_p], None]
    class internal_3:
        le_next: ctypes._Pointer[Notifier]
        le_prev: ctypes._Pointer[ctypes._Pointer[Notifier]]

    node: internal_3

class Object:
    klass: ctypes.c_void_p
    free: ctypes.c_void_p
    properties: ctypes.c_void_p
    ref: ctypes.c_uint
    parent: ctypes.c_void_p

class OsiModule:
    modd: ctypes.c_uint
    base: ctypes.c_uint
    size: ctypes.c_uint
    file: ctypes._Pointer[ctypes.c_char]
    name: ctypes._Pointer[ctypes.c_char]
    offset: ctypes.c_uint
    flags: ctypes.c_uint

class OsiPage:
    start: ctypes.c_uint
    len: ctypes.c_uint

class OsiProc:
    taskd: ctypes.c_uint
    pgd: ctypes.c_uint
    asid: ctypes.c_uint
    pid: ctypes.c_int
    ppid: ctypes.c_int
    name: ctypes._Pointer[ctypes.c_char]
    pages: ctypes._Pointer[osi_page_struct]
    create_time: ctypes.c_ulong

class OsiProcHandle:
    taskd: ctypes.c_uint
    asid: ctypes.c_uint

class OsiProcMem:
    start_brk: ctypes.c_uint
    brk: ctypes.c_uint

class OsiThread:
    pid: ctypes.c_int
    tid: ctypes.c_int

PAddr: ctypes.c_ulong
class PandaOsFamily(IntEnum):
    OS_FREEBSD: int = 3
    OS_LINUX: int = 2
    OS_WINDOWS: int = 1
    OS_UNKNOWN: int = 0

class Path:
    dentry: ctypes.c_uint
    mnt: ctypes.c_uint

QDict: ctypes.Array[ctypes.c_ubyte]
QEMUClockType: ctypes.c_uint
QEMUTimerCB: None
QEMUTimerListNotifyCB: None
class QObject:
    type: ctypes.c_uint
    refcnt: ctypes.c_ulong

class QString:
    base: QObject
    string: ctypes._Pointer[ctypes.c_char]
    length: ctypes.c_ulong
    capacity: ctypes.c_ulong

QType: ctypes.c_uint
class QemuCond:
    cond: ctypes.Array[ctypes.c_ubyte]

class QemuMutex:
    lock: ctypes.Array[ctypes.c_ubyte]

class QemuOptDesc:
    name: ctypes._Pointer[ctypes.c_char]
    type: QemuOptType
    help: ctypes._Pointer[ctypes.c_char]
    def_value_str: ctypes._Pointer[ctypes.c_char]

class QemuOptHead:
    tqh_first: ctypes._Pointer[QemuOpt]
    tqh_last: ctypes._Pointer[ctypes._Pointer[QemuOpt]]

class QemuOpts:
    id: ctypes._Pointer[ctypes.c_char]
    list: ctypes._Pointer[QemuOptsList]
    loc: Location
    head: QemuOptHead
    class internal_15:
        tqe_next: ctypes._Pointer[QemuOpts]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[QemuOpts]]

    next: internal_15

class QemuOptsList:
    name: ctypes._Pointer[ctypes.c_char]
    implied_opt_name: ctypes._Pointer[ctypes.c_char]
    merge_lists: ctypes.c_bool
    class internal_8:
        tqh_first: ctypes._Pointer[QemuOpts]
        tqh_last: ctypes._Pointer[ctypes._Pointer[QemuOpts]]

    head: internal_8
    desc: ctypes.Array[QemuOptDesc]

class QemuThread:
    thread: ctypes.c_ulong

class QueryResult:
    num_labels: ctypes.c_uint
    ls: ctypes.c_void_p
    it_end: ctypes.c_void_p
    it_curr: ctypes.c_void_p
    tcn: ctypes.c_uint
    cb_mask: ctypes.c_ubyte

class RAMBlock:
    rcu: rcu_head
    mr: ctypes._Pointer[MemoryRegion]
    host: ctypes._Pointer[ctypes.c_ubyte]
    offset: ctypes.c_ulong
    used_length: ctypes.c_ulong
    max_length: ctypes.c_ulong
    resized: Callable[[ctypes._Pointer[ctypes.c_char], ctypes.c_ulong, ctypes.c_void_p], None]
    flags: ctypes.c_uint
    idstr: ctypes.Array[ctypes.c_char]
    class internal_1:
        le_next: ctypes._Pointer[RAMBlock]
        le_prev: ctypes._Pointer[ctypes._Pointer[RAMBlock]]

    next: internal_1
    class internal_2:
        lh_first: ctypes._Pointer[RAMBlockNotifier]

    ramblock_notifiers: internal_2
    fd: ctypes.c_int
    page_size: ctypes.c_ulong

RCUCBFunc: None
class RRCTRL_ret(IntEnum):
    RRCTRL_OK: int = 0
    RRCTRL_EPENDING: int = -1
    RRCTRL_EINVALID: int = -2

class RR_mem_type(IntEnum):
    RR_MEM_UNKNOWN: int = 2
    RR_MEM_RAM: int = 1
    RR_MEM_IO: int = 0

class RR_mode(IntEnum):
    RR_REPLAY: int = 2
    RR_RECORD: int = 1
    RR_OFF: int = 0
    RR_NOCHANGE: int = -1

ReadLineCompletionFunc: None
ReadLineFlushFunc: None
ReadLineFunc: None
ReadLinePrintfFunc: None
class ReadLineState:
    cmd_buf: ctypes.Array[ctypes.c_char]
    cmd_buf_index: ctypes.c_int
    cmd_buf_size: ctypes.c_int
    last_cmd_buf: ctypes.Array[ctypes.c_char]
    last_cmd_buf_index: ctypes.c_int
    last_cmd_buf_size: ctypes.c_int
    esc_state: ctypes.c_int
    esc_param: ctypes.c_int
    history: ctypes.Array[ctypes._Pointer[ctypes.c_char]]
    hist_entry: ctypes.c_int
    completion_finder: Callable[[ctypes.c_void_p, ctypes._Pointer[ctypes.c_char]], None]
    completions: ctypes.Array[ctypes._Pointer[ctypes.c_char]]
    nb_completions: ctypes.c_int
    completion_index: ctypes.c_int
    readline_func: Callable[[ctypes.c_void_p, ctypes._Pointer[ctypes.c_char], ctypes.c_void_p], None]
    readline_opaque: ctypes.c_void_p
    read_password: ctypes.c_int
    prompt: ctypes.Array[ctypes.c_char]
    printf_func: Callable[[ctypes.c_void_p, ctypes._Pointer[ctypes.c_char]], None]
    flush_func: Callable[[ctypes.c_void_p], None]
    opaque: ctypes.c_void_p

Ret: ctypes.c_ulong
class SegmentCache:
    selector: ctypes.c_uint
    base: ctypes.c_uint
    limit: ctypes.c_uint
    flags: ctypes.c_uint

class String:
    pass

class SymbolicBranchMeta:
    pc: ctypes.c_ulong

TCGMemOp: ctypes.c_uint
class TCR:
    raw_tcr: ctypes.c_ulong
    mask: ctypes.c_uint
    base_mask: ctypes.c_uint

class TPRAccess(IntEnum):
    TPR_ACCESS_WRITE: int = 1
    TPR_ACCESS_READ: int = 0

TaintLabel: ctypes.c_uint
class TaskStruct:
    tasks: ListHead
    pid: ctypes.c_uint
    tgid: ctypes.c_uint
    group_leader: ctypes.c_uint
    thread_group: ctypes.c_uint
    real_parent: ctypes.c_uint
    parent: ctypes.c_uint
    mm: ctypes.c_uint
    stack: ctypes.c_uint
    real_cred: ctypes.c_uint
    cred: ctypes.c_uint
    comm: ctypes.Array[ctypes.c_ubyte]
    files: ctypes.c_uint
    start_time: ctypes.c_uint
    children: ListHead
    sibling: ListHead

class TranslationBlock:
    pc: ctypes.c_uint
    cs_base: ctypes.c_uint
    flags: ctypes.c_uint
    size: ctypes.c_ushort
    icount: ctypes.c_ushort
    cflags: ctypes.c_uint
    invalid: ctypes.c_ushort
    was_split: ctypes.c_ubyte
    tc_ptr: ctypes.c_void_p
    tc_search: ctypes._Pointer[ctypes.c_ubyte]
    orig_tb: ctypes._Pointer[TranslationBlock]
    page_next: ctypes.Array[ctypes._Pointer[TranslationBlock]]
    page_addr: ctypes.Array[ctypes.c_ulong]
    jmp_reset_offset: ctypes.Array[ctypes.c_ushort]
    jmp_insn_offset: ctypes.Array[ctypes.c_ushort]
    jmp_list_next: ctypes.Array[ctypes.c_ulong]
    jmp_list_first: ctypes.c_ulong
    llvm_tc_ptr: ctypes._Pointer[ctypes.c_ubyte]
    llvm_tc_end: ctypes._Pointer[ctypes.c_ubyte]
    llvm_tb_next: ctypes.Array[ctypes._Pointer[TranslationBlock]]
    llvm_asm_ptr: ctypes._Pointer[ctypes.c_ubyte]
    llvm_fn_name: ctypes.Array[ctypes.c_char]

Unk: ctypes.c_ulong
ValueUnion: ctypes.c_ulong
class Vec_CosiModule:
    pass

class Vec_CosiProc:
    pass

class VmAreaStruct:
    vm_mm: ctypes.c_uint
    vm_start: ctypes.c_uint
    vm_end: ctypes.c_uint
    vm_next: ctypes.c_uint
    vm_file: ctypes.c_uint
    vm_flags: ctypes.c_uint

class VolatilityBaseType:
    pass

class VolatilityEnum:
    pass

class VolatilityStruct:
    pass

class VolatilitySymbol:
    pass

ZMMReg: ctypes.Array[ctypes.c_ubyte]
__u16: ctypes.c_ushort
__u32: ctypes.c_uint
__u64: ctypes.c_ulong
__u8: ctypes.c_ubyte
_add_hooks2_t: Callable[[Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes.c_void_p], ctypes.c_bool], ctypes.c_void_p, ctypes.c_bool, ctypes._Pointer[ctypes.c_char], ctypes._Pointer[ctypes.c_char], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], ctypes.c_int]
_disable_hooks2_t: Callable[[ctypes.c_int], None]
_enable_hooks2_t: Callable[[ctypes.c_int], None]
class breakpoints_head:
    tqh_first: ctypes._Pointer[CPUBreakpoint]
    tqh_last: ctypes._Pointer[ctypes._Pointer[CPUBreakpoint]]

class coalesced_ranges:
    tqh_first: ctypes._Pointer[CoalescedMemoryRange]
    tqh_last: ctypes._Pointer[ctypes._Pointer[CoalescedMemoryRange]]

dcr_read_cb: Callable[[ctypes.c_void_p, ctypes.c_int], ctypes.c_uint]
dcr_write_cb: Callable[[ctypes.c_void_p, ctypes.c_int, ctypes.c_uint], None]
dynamic_hook_func_t: Callable[[ctypes._Pointer[hook_symbol_resolve], symbol, ctypes.c_uint], None]
dynamic_symbol_hook_func_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[hook]], ctypes.c_bool]
flag: ctypes.c_char
float32: ctypes.c_uint
float64: ctypes.c_ulong
class float_status:
    float_detect_tininess: ctypes.c_byte
    float_rounding_mode: ctypes.c_byte
    float_exception_flags: ctypes.c_ubyte
    floatx80_rounding_precision: ctypes.c_byte
    flush_to_zero: ctypes.c_char
    flush_inputs_to_zero: ctypes.c_char
    default_nan_mode: ctypes.c_char
    snan_bit_is_one: ctypes.c_char

class floatx80:
    low: ctypes.c_ulong
    high: ctypes.c_ushort

fpr_t: ctypes.Array[ctypes.c_ubyte]
gchar: ctypes.c_char
gdb_reg_cb: ctypes.c_int
guint: ctypes.c_uint
hax_fd: ctypes.c_ulong
class hax_global:
    pass

class hax_vcpu_state:
    fd: ctypes.c_ulong
    vcpu_id: ctypes.c_int
    tunnel: ctypes._Pointer[hax_tunnel]
    iobuf: ctypes._Pointer[ctypes.c_ubyte]

class hook:
    addr: ctypes.c_uint
    asid: ctypes.c_uint
    type: panda_cb_type
    cb: hooks_panda_cb
    km: kernel_mode
    enabled: ctypes.c_bool
    sym: symbol
    context: ctypes.c_void_p

hook_func_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[hook]], ctypes.c_bool]
hooks2_func_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes.c_void_p], ctypes.c_bool]
class hooks_panda_cb:
    before_tcg_codegen: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[hook]], None]
    before_block_translate: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes._Pointer[hook]], None]
    after_block_translate: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[hook]], None]
    before_block_exec_invalidate_opt: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[hook]], ctypes.c_bool]
    before_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[hook]], None]
    after_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes.c_ubyte, ctypes._Pointer[hook]], None]
    start_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[hook]], None]
    end_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[hook]], None]

hwaddr: ctypes.c_ulong
hypercall_t: Callable[[ctypes._Pointer[CPUState]], None]
class icount_decr_u16:
    low: ctypes.c_ushort
    high: ctypes.c_ushort

mem_hook_func_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[memory_access_desc]], None]
class memory_listeners_as:
    tqh_first: ctypes._Pointer[MemoryListener]
    tqh_last: ctypes._Pointer[ctypes._Pointer[MemoryListener]]

mon_cmd_t: ctypes.Array[ctypes.c_ubyte]
on_NtAcceptConnectPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAcceptConnectPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAccessCheckAndAuditAlarm_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAccessCheckAndAuditAlarm_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAccessCheckByTypeAndAuditAlarm_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAccessCheckByTypeAndAuditAlarm_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAccessCheckByTypeResultListAndAuditAlarmByHandle_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAccessCheckByTypeResultListAndAuditAlarmByHandle_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAccessCheckByTypeResultListAndAuditAlarm_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAccessCheckByTypeResultListAndAuditAlarm_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAccessCheckByTypeResultList_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAccessCheckByTypeResultList_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAccessCheckByType_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAccessCheckByType_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAccessCheck_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAccessCheck_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAddAtom_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAddAtom_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAddBootEntry_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAddBootEntry_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAddDriverEntry_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAddDriverEntry_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAdjustGroupsToken_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAdjustGroupsToken_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAdjustPrivilegesToken_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAdjustPrivilegesToken_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlertResumeThread_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlertResumeThread_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlertThread_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtAlertThread_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtAllocateLocallyUniqueId_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtAllocateLocallyUniqueId_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtAllocateReserveObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAllocateReserveObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAllocateUserPhysicalPages_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAllocateUserPhysicalPages_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAllocateUuids_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAllocateUuids_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAllocateVirtualMemory_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAllocateVirtualMemory_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcAcceptConnectPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcAcceptConnectPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcCancelMessage_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcCancelMessage_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcConnectPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcConnectPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcCreatePortSection_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcCreatePortSection_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcCreatePort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcCreatePort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcCreateResourceReserve_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcCreateResourceReserve_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcCreateSectionView_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcCreateSectionView_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcCreateSecurityContext_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcCreateSecurityContext_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcDeletePortSection_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcDeletePortSection_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcDeleteResourceReserve_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcDeleteResourceReserve_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcDeleteSectionView_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcDeleteSectionView_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcDeleteSecurityContext_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcDeleteSecurityContext_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcDisconnectPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcDisconnectPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcImpersonateClientOfPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcImpersonateClientOfPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcOpenSenderProcess_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcOpenSenderProcess_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcOpenSenderThread_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcOpenSenderThread_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcQueryInformationMessage_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcQueryInformationMessage_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcQueryInformation_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcQueryInformation_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcRevokeSecurityContext_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcRevokeSecurityContext_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcSendWaitReceivePort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcSendWaitReceivePort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcSetInformation_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAlpcSetInformation_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtApphelpCacheControl_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtApphelpCacheControl_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAreMappedFilesTheSame_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAreMappedFilesTheSame_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAssignProcessToJobObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtAssignProcessToJobObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCallbackReturn_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCallbackReturn_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCancelIoFileEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCancelIoFileEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCancelIoFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCancelIoFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCancelSynchronousIoFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCancelSynchronousIoFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCancelTimer_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCancelTimer_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtClearEvent_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtClearEvent_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtCloseObjectAuditAlarm_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCloseObjectAuditAlarm_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtClose_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtClose_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtCommitComplete_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCommitComplete_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCommitEnlistment_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCommitEnlistment_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCommitTransaction_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCommitTransaction_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCompactKeys_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCompactKeys_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCompareTokens_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCompareTokens_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCompleteConnectPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtCompleteConnectPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtCompressKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtCompressKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtConnectPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtConnectPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtContinue_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtContinue_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateDebugObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateDebugObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateDirectoryObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateDirectoryObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateEnlistment_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateEnlistment_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateEventPair_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateEventPair_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateEvent_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateEvent_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateIoCompletion_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateIoCompletion_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateJobObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateJobObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateJobSet_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateJobSet_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateKeyTransacted_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateKeyTransacted_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateKeyedEvent_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateKeyedEvent_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateMailslotFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateMailslotFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateMutant_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateMutant_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateNamedPipeFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateNamedPipeFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreatePagingFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreatePagingFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreatePort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreatePort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreatePrivateNamespace_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreatePrivateNamespace_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateProcessEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateProcessEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateProcess_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateProcess_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateProfileEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateProfileEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateProfile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateProfile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateResourceManager_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateResourceManager_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateSection_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateSection_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateSemaphore_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_NtCreateSemaphore_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_NtCreateSymbolicLinkObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateSymbolicLinkObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateThreadEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateThreadEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateThread_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateThread_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateTimer_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateTimer_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateToken_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateToken_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateTransactionManager_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateTransactionManager_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateTransaction_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateTransaction_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateUserProcess_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateUserProcess_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateWaitablePort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateWaitablePort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateWorkerFactory_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtCreateWorkerFactory_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDebugActiveProcess_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDebugActiveProcess_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDebugContinue_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDebugContinue_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDelayExecution_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDelayExecution_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDeleteAtom_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDeleteAtom_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDeleteBootEntry_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDeleteBootEntry_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDeleteDriverEntry_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDeleteDriverEntry_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDeleteFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDeleteFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDeleteKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDeleteKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDeleteObjectAuditAlarm_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDeleteObjectAuditAlarm_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDeletePrivateNamespace_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDeletePrivateNamespace_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDeleteValueKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDeleteValueKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDeviceIoControlFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDeviceIoControlFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDisableLastKnownGood_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtDisableLastKnownGood_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtDisplayString_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDisplayString_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDrawText_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDrawText_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtDuplicateObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDuplicateObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDuplicateToken_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtDuplicateToken_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtEnableLastKnownGood_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtEnableLastKnownGood_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtEnumerateBootEntries_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtEnumerateBootEntries_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtEnumerateDriverEntries_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtEnumerateDriverEntries_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtEnumerateKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtEnumerateKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtEnumerateSystemEnvironmentValuesEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtEnumerateSystemEnvironmentValuesEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtEnumerateTransactionObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtEnumerateTransactionObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtEnumerateValueKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtEnumerateValueKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtExtendSection_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtExtendSection_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFilterToken_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFilterToken_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFindAtom_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFindAtom_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFlushBuffersFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFlushBuffersFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFlushInstallUILanguage_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFlushInstallUILanguage_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFlushInstructionCache_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFlushInstructionCache_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFlushKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtFlushKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtFlushProcessWriteBuffers_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtFlushProcessWriteBuffers_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtFlushVirtualMemory_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFlushVirtualMemory_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFlushWriteBuffer_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtFlushWriteBuffer_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtFreeUserPhysicalPages_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFreeUserPhysicalPages_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFreeVirtualMemory_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFreeVirtualMemory_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFreezeRegistry_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtFreezeRegistry_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtFreezeTransactions_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFreezeTransactions_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFsControlFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtFsControlFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetContextThread_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetContextThread_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetCurrentProcessorNumber_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtGetCurrentProcessorNumber_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtGetDevicePowerState_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetDevicePowerState_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetMUIRegistryInfo_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetMUIRegistryInfo_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetNextProcess_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetNextProcess_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetNextThread_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetNextThread_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetNlsSectionPtr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetNlsSectionPtr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetNotificationResourceManager_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetNotificationResourceManager_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetPlugPlayEvent_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetPlugPlayEvent_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetWriteWatch_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtGetWriteWatch_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtImpersonateAnonymousToken_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtImpersonateAnonymousToken_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtImpersonateClientOfPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtImpersonateClientOfPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtImpersonateThread_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtImpersonateThread_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtInitializeNlsFiles_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtInitializeNlsFiles_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtInitializeRegistry_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtInitializeRegistry_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtInitiatePowerAction_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtInitiatePowerAction_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtIsProcessInJob_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtIsProcessInJob_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtIsSystemResumeAutomatic_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtIsSystemResumeAutomatic_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtIsUILanguageComitted_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtIsUILanguageComitted_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtListenPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtListenPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtLoadDriver_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtLoadDriver_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtLoadKey2_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtLoadKey2_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtLoadKeyEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtLoadKeyEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtLoadKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtLoadKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtLockFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtLockFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtLockProductActivationKeys_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtLockProductActivationKeys_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtLockRegistryKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtLockRegistryKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtLockVirtualMemory_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtLockVirtualMemory_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtMakePermanentObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtMakePermanentObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtMakeTemporaryObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtMakeTemporaryObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtMapCMFModule_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtMapCMFModule_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtMapUserPhysicalPagesScatter_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtMapUserPhysicalPagesScatter_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtMapUserPhysicalPages_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtMapUserPhysicalPages_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtMapViewOfSection_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtMapViewOfSection_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtModifyBootEntry_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtModifyBootEntry_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtModifyDriverEntry_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtModifyDriverEntry_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtNotifyChangeDirectoryFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtNotifyChangeDirectoryFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtNotifyChangeKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtNotifyChangeKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtNotifyChangeMultipleKeys_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtNotifyChangeMultipleKeys_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtNotifyChangeSession_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtNotifyChangeSession_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenDirectoryObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenDirectoryObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenEnlistment_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenEnlistment_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenEventPair_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenEventPair_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenEvent_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenEvent_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenIoCompletion_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenIoCompletion_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenJobObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenJobObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenKeyEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenKeyEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenKeyTransactedEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenKeyTransactedEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenKeyTransacted_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenKeyTransacted_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenKeyedEvent_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenKeyedEvent_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenMutant_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenMutant_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenObjectAuditAlarm_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenObjectAuditAlarm_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenPrivateNamespace_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenPrivateNamespace_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenProcessTokenEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenProcessTokenEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenProcessToken_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenProcessToken_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenProcess_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenProcess_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenResourceManager_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenResourceManager_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenSection_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenSection_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenSemaphore_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenSemaphore_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenSession_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenSession_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenSymbolicLinkObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenSymbolicLinkObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenThreadTokenEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenThreadTokenEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenThreadToken_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenThreadToken_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenThread_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenThread_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenTimer_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenTimer_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenTransactionManager_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenTransactionManager_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenTransaction_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtOpenTransaction_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPlugPlayControl_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPlugPlayControl_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPowerInformation_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPowerInformation_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPrePrepareComplete_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPrePrepareComplete_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPrePrepareEnlistment_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPrePrepareEnlistment_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPrepareComplete_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPrepareComplete_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPrepareEnlistment_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPrepareEnlistment_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPrivilegeCheck_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPrivilegeCheck_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPrivilegeObjectAuditAlarm_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPrivilegeObjectAuditAlarm_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPrivilegedServiceAuditAlarm_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPrivilegedServiceAuditAlarm_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPropagationComplete_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPropagationComplete_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPropagationFailed_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPropagationFailed_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtProtectVirtualMemory_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtProtectVirtualMemory_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPulseEvent_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtPulseEvent_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryAttributesFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryAttributesFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryBootEntryOrder_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryBootEntryOrder_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryBootOptions_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryBootOptions_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryDebugFilterState_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryDebugFilterState_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryDefaultLocale_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryDefaultLocale_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryDefaultUILanguage_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryDefaultUILanguage_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryDirectoryFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryDirectoryFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryDirectoryObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryDirectoryObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryDriverEntryOrder_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryDriverEntryOrder_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryEaFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryEaFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryEvent_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryEvent_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryFullAttributesFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryFullAttributesFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationAtom_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationAtom_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationEnlistment_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationEnlistment_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationJobObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationJobObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationProcess_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationProcess_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationResourceManager_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationResourceManager_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationThread_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationThread_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationToken_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationToken_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationTransactionManager_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationTransactionManager_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationTransaction_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationTransaction_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationWorkerFactory_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInformationWorkerFactory_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInstallUILanguage_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryInstallUILanguage_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryIntervalProfile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryIntervalProfile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryIoCompletion_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryIoCompletion_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryLicenseValue_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryLicenseValue_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryMultipleValueKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryMultipleValueKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryMutant_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryMutant_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryOpenSubKeysEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryOpenSubKeysEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryOpenSubKeys_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryOpenSubKeys_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryPerformanceCounter_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryPerformanceCounter_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryPortInformationProcess_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtQueryPortInformationProcess_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtQueryQuotaInformationFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryQuotaInformationFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySection_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySection_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySecurityAttributesToken_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySecurityAttributesToken_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySecurityObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySecurityObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySemaphore_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySemaphore_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySymbolicLinkObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySymbolicLinkObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySystemEnvironmentValueEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySystemEnvironmentValueEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySystemEnvironmentValue_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySystemEnvironmentValue_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySystemInformationEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySystemInformationEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySystemInformation_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySystemInformation_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySystemTime_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtQuerySystemTime_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryTimerResolution_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryTimerResolution_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryTimer_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryTimer_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryValueKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryValueKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryVirtualMemory_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryVirtualMemory_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryVolumeInformationFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueryVolumeInformationFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueueApcThreadEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueueApcThreadEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueueApcThread_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtQueueApcThread_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRaiseException_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRaiseException_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRaiseHardError_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRaiseHardError_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReadFileScatter_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReadFileScatter_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReadFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReadFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReadOnlyEnlistment_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReadOnlyEnlistment_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReadRequestData_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReadRequestData_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReadVirtualMemory_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReadVirtualMemory_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRecoverEnlistment_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRecoverEnlistment_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRecoverResourceManager_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtRecoverResourceManager_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtRecoverTransactionManager_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtRecoverTransactionManager_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtRegisterProtocolAddressInformation_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRegisterProtocolAddressInformation_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRegisterThreadTerminatePort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtRegisterThreadTerminatePort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtReleaseKeyedEvent_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReleaseKeyedEvent_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReleaseMutant_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReleaseMutant_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReleaseSemaphore_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_NtReleaseSemaphore_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_NtReleaseWorkerFactoryWorker_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtReleaseWorkerFactoryWorker_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtRemoveIoCompletionEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRemoveIoCompletionEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRemoveIoCompletion_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRemoveIoCompletion_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRemoveProcessDebug_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRemoveProcessDebug_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRenameKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRenameKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRenameTransactionManager_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRenameTransactionManager_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReplaceKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReplaceKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReplacePartitionUnit_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReplacePartitionUnit_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReplyPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReplyPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReplyWaitReceivePortEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReplyWaitReceivePortEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReplyWaitReceivePort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReplyWaitReceivePort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReplyWaitReplyPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtReplyWaitReplyPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRequestPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRequestPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRequestWaitReplyPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRequestWaitReplyPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtResetEvent_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtResetEvent_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtResetWriteWatch_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtResetWriteWatch_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRestoreKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRestoreKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtResumeProcess_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtResumeProcess_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtResumeThread_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtResumeThread_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRollbackComplete_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRollbackComplete_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRollbackEnlistment_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRollbackEnlistment_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRollbackTransaction_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRollbackTransaction_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRollforwardTransactionManager_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtRollforwardTransactionManager_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSaveKeyEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSaveKeyEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSaveKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSaveKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSaveMergedKeys_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSaveMergedKeys_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSecureConnectPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSecureConnectPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSerializeBoot_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtSerializeBoot_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtSetBootEntryOrder_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetBootEntryOrder_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetBootOptions_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetBootOptions_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetContextThread_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetContextThread_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetDebugFilterState_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetDebugFilterState_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetDefaultHardErrorPort_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetDefaultHardErrorPort_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetDefaultLocale_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetDefaultLocale_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetDefaultUILanguage_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetDefaultUILanguage_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetDriverEntryOrder_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetDriverEntryOrder_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetEaFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetEaFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetEventBoostPriority_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetEventBoostPriority_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetEvent_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetEvent_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetHighEventPair_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetHighEventPair_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetHighWaitLowEventPair_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetHighWaitLowEventPair_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationDebugObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationDebugObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationEnlistment_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationEnlistment_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationJobObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationJobObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationProcess_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationProcess_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationResourceManager_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationResourceManager_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationThread_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationThread_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationToken_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationToken_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationTransactionManager_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationTransactionManager_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationTransaction_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationTransaction_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationWorkerFactory_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetInformationWorkerFactory_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetIntervalProfile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetIntervalProfile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetIoCompletionEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetIoCompletionEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetIoCompletion_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetIoCompletion_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetLdtEntries_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetLdtEntries_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetLowEventPair_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetLowEventPair_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetLowWaitHighEventPair_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetLowWaitHighEventPair_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetQuotaInformationFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetQuotaInformationFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetSecurityObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetSecurityObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetSystemEnvironmentValueEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetSystemEnvironmentValueEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetSystemEnvironmentValue_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetSystemEnvironmentValue_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetSystemInformation_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetSystemInformation_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetSystemPowerState_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetSystemPowerState_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetSystemTime_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetSystemTime_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetThreadExecutionState_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetThreadExecutionState_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetTimerEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetTimerEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetTimerResolution_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetTimerResolution_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetTimer_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_NtSetTimer_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_NtSetUuidSeed_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetUuidSeed_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSetValueKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetValueKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetVolumeInformationFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSetVolumeInformationFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtShutdownSystem_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtShutdownSystem_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtShutdownWorkerFactory_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtShutdownWorkerFactory_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSignalAndWaitForSingleObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSignalAndWaitForSingleObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSinglePhaseReject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSinglePhaseReject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtStartProfile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtStartProfile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtStopProfile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtStopProfile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSuspendProcess_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSuspendProcess_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtSuspendThread_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSuspendThread_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSystemDebugControl_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtSystemDebugControl_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtTerminateJobObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtTerminateJobObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtTerminateProcess_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtTerminateProcess_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtTerminateThread_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtTerminateThread_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtTestAlert_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtTestAlert_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtThawRegistry_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtThawRegistry_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtThawTransactions_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtThawTransactions_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtTraceControl_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtTraceControl_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtTraceEvent_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtTraceEvent_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtTranslateFilePath_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtTranslateFilePath_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtUmsThreadYield_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtUmsThreadYield_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtUnloadDriver_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtUnloadDriver_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtUnloadKey2_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtUnloadKey2_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtUnloadKeyEx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtUnloadKeyEx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtUnloadKey_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtUnloadKey_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtUnlockFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtUnlockFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtUnlockVirtualMemory_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtUnlockVirtualMemory_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtUnmapViewOfSection_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtUnmapViewOfSection_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtVdmControl_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtVdmControl_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitForDebugEvent_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitForDebugEvent_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitForKeyedEvent_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitForKeyedEvent_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitForMultipleObjects32_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitForMultipleObjects32_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitForMultipleObjects_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitForMultipleObjects_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitForSingleObject_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitForSingleObject_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitForWorkViaWorkerFactory_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitForWorkViaWorkerFactory_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitHighEventPair_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitHighEventPair_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitLowEventPair_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtWaitLowEventPair_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtWorkerFactoryWorkerReady_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtWorkerFactoryWorkerReady_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_NtWriteFileGather_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWriteFileGather_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWriteFile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWriteFile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWriteRequestData_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWriteRequestData_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWriteVirtualMemory_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtWriteVirtualMemory_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_NtYieldExecution_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_NtYieldExecution_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_after_load_t: Callable[[addr_struct, ctypes.c_ulong, ctypes.c_ulong], None]
on_after_store_t: Callable[[addr_struct, ctypes.c_ulong, ctypes.c_ulong], None]
on_all_sys_enter2_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes._Pointer[syscall_info_t], ctypes._Pointer[syscall_ctx]], None]
on_all_sys_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_all_sys_return2_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes._Pointer[syscall_info_t], ctypes._Pointer[syscall_ctx]], None]
on_all_sys_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_branch2_t: Callable[[addr_struct, ctypes.c_ulong, ctypes.c_bool, ctypes._Pointer[ctypes.c_bool]], None]
on_branch_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes.c_ulong], ctypes.c_bool]
on_call_match_num_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes._Pointer[ctypes.c_uint], ctypes.c_uint, ctypes.c_uint], None]
on_call_match_str_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes._Pointer[ctypes.c_uint], ctypes._Pointer[ctypes.c_char], ctypes.c_uint, ctypes.c_uint], None]
on_call_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_get_current_process_handle_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes._Pointer[osi_proc_handle_struct]]], None]
on_get_current_process_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes._Pointer[osi_proc_struct]]], None]
on_get_current_thread_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes._Pointer[osi_thread_struct]]], None]
on_get_file_mappings_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[osi_proc_struct], ctypes._Pointer[ctypes.c_void_p]], None]
on_get_heap_mappings_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[osi_proc_struct], ctypes._Pointer[ctypes.c_void_p]], None]
on_get_mapping_base_address_by_name_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[osi_proc_struct], ctypes._Pointer[ctypes.c_char], ctypes._Pointer[ctypes.c_uint]], None]
on_get_mapping_by_addr_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[osi_proc_struct], ctypes.c_uint, ctypes._Pointer[ctypes._Pointer[osi_module_struct]]], None]
on_get_mappings_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[osi_proc_struct], ctypes._Pointer[ctypes.c_void_p]], None]
on_get_modules_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_void_p]], None]
on_get_proc_mem_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[osi_proc_struct], ctypes._Pointer[ctypes._Pointer[osi_proc_mem]]], None]
on_get_process_handles_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_void_p]], None]
on_get_process_pid_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[osi_proc_handle_struct], ctypes._Pointer[ctypes.c_int]], None]
on_get_process_ppid_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[osi_proc_handle_struct], ctypes._Pointer[ctypes.c_int]], None]
on_get_process_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[osi_proc_handle_struct], ctypes._Pointer[ctypes._Pointer[osi_proc_struct]]], None]
on_get_processes_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_void_p]], None]
on_get_stack_mappings_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[osi_proc_struct], ctypes._Pointer[ctypes.c_void_p]], None]
on_get_unknown_mappings_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[osi_proc_struct], ctypes._Pointer[ctypes.c_void_p]], None]
on_has_mapping_prefix_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[osi_proc_struct], ctypes._Pointer[ctypes.c_char], ctypes._Pointer[ctypes.c_bool]], None]
on_indirect_jump_t: Callable[[addr_struct, ctypes.c_ulong, ctypes.c_bool, ctypes._Pointer[ctypes.c_bool]], None]
on_mmap_updated_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_char], ctypes.c_uint, ctypes.c_uint], None]
on_process_end_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_char], ctypes.c_uint, ctypes.c_int], None]
on_process_start_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_char], ctypes.c_uint, ctypes.c_int], None]
on_ptr_load_t: Callable[[addr_struct, ctypes.c_ulong, ctypes.c_ulong], None]
on_ptr_store_t: Callable[[addr_struct, ctypes.c_ulong, ctypes.c_ulong], None]
on_rec_auxv_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[auxv_values]], None]
on_ret_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_ssm_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes._Pointer[ctypes.c_ubyte], ctypes.c_uint, ctypes.c_bool, ctypes.c_bool], None]
on_sys_accept4_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_accept4_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_access_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_access_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_acct_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_acct_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_add_key_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_add_key_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_adjtimex_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_adjtimex_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_alarm_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_alarm_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_arch_prctl_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_arch_prctl_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_bdflush_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_bdflush_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_bind_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_bind_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_bpf_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_bpf_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_brk_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_brk_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_capget_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_capget_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_capset_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_capset_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_chdir_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_chdir_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_chmod_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_chmod_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_chown16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_chown16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_chown_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_chown_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_chroot_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_chroot_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_clock_adjtime_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_clock_adjtime_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_clock_getres_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_clock_getres_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_clock_gettime_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_clock_gettime_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_clock_nanosleep_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_clock_nanosleep_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_clock_settime_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_clock_settime_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_clone_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_clone_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_close_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_close_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_connect_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_connect_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_copy_file_range_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_copy_file_range_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_creat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_creat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_delete_module_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_delete_module_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_dup2_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_dup2_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_dup3_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_dup3_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_dup_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_dup_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_epoll_create1_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_epoll_create1_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_epoll_create_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_epoll_create_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_epoll_ctl_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint], None]
on_sys_epoll_ctl_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint], None]
on_sys_epoll_pwait_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_epoll_pwait_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_epoll_wait_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_epoll_wait_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_eventfd2_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_eventfd2_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_eventfd_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_eventfd_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_execve_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_execve_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_execveat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_execveat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_exit_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_exit_group_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_exit_group_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_exit_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_faccessat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_faccessat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_fadvise64_64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_int], None]
on_sys_fadvise64_64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_int], None]
on_sys_fadvise64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_ulong, ctypes.c_uint, ctypes.c_int], None]
on_sys_fadvise64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_ulong, ctypes.c_uint, ctypes.c_int], None]
on_sys_fallocate_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong], None]
on_sys_fallocate_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong], None]
on_sys_fanotify_init_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fanotify_init_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fanotify_mark_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_ulong, ctypes.c_int, ctypes.c_uint], None]
on_sys_fanotify_mark_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_ulong, ctypes.c_int, ctypes.c_uint], None]
on_sys_fchdir_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_fchdir_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_fchmod_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fchmod_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fchmodat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fchmodat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fchown16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fchown16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fchown_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fchown_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fchownat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_fchownat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_fcntl64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fcntl64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fcntl_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fcntl_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fdatasync_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_fdatasync_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_fgetxattr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fgetxattr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_finit_module_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_finit_module_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_flistxattr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_flistxattr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_flock_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_flock_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fork_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_fork_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_fremovexattr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_fremovexattr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_fsetxattr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_fsetxattr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_fstat64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fstat64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fstat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fstat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fstatat64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_fstatat64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_fstatfs64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fstatfs64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fstatfs_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fstatfs_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_fsync_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_fsync_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_ftruncate64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
on_sys_ftruncate64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
on_sys_ftruncate_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_ftruncate_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_futex_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_futex_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_futimesat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_futimesat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_get_mempolicy_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_get_mempolicy_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_get_robust_list_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_get_robust_list_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_get_thread_area_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_get_thread_area_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_getcpu_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getcpu_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getcwd_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getcwd_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getdents64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getdents64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getdents_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getdents_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getegid16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getegid16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getegid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getegid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_geteuid16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_geteuid16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_geteuid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_geteuid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getgid16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getgid16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getgid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getgid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getgroups16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_getgroups16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_getgroups_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_getgroups_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_getitimer_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_getitimer_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_getpeername_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getpeername_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getpgid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_getpgid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_getpgrp_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getpgrp_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getpid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getpid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getppid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getppid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getpriority_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_getpriority_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_getrandom_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getrandom_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getresgid16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getresgid16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getresgid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getresgid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getresuid16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getresuid16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getresuid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getresuid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getrlimit_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getrlimit_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getrusage_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_getrusage_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_getsid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_getsid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_getsockname_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getsockname_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getsockopt_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getsockopt_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_gettid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_gettid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_gettimeofday_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_gettimeofday_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getuid16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getuid16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getuid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getuid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_getxattr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_getxattr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_init_module_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_init_module_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_inotify_add_watch_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_inotify_add_watch_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_inotify_init1_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_inotify_init1_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_inotify_init_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_inotify_init_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_inotify_rm_watch_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_inotify_rm_watch_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_io_cancel_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_io_cancel_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_io_destroy_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_io_destroy_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_io_getevents_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_io_getevents_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_io_setup_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_io_setup_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_io_submit_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_io_submit_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_ioctl_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_ioctl_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_ioperm_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_ioperm_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_iopl_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_iopl_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_ioprio_get_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_ioprio_get_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_ioprio_set_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int], None]
on_sys_ioprio_set_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int], None]
on_sys_ipc_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_ipc_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_kcmp_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_kcmp_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_kexec_load_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_kexec_load_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_keyctl_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_keyctl_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_kill_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_kill_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_lchown16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_lchown16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_lchown_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_lchown_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_lgetxattr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_lgetxattr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_link_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_link_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_linkat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_linkat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_listen_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_listen_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_listxattr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_listxattr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_llistxattr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_llistxattr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_llseek_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_llseek_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_lookup_dcookie_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ulong, ctypes.c_uint, ctypes.c_uint], None]
on_sys_lookup_dcookie_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ulong, ctypes.c_uint, ctypes.c_uint], None]
on_sys_lremovexattr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_lremovexattr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_lseek_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_lseek_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_lsetxattr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_lsetxattr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_lstat64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_lstat64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_lstat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_lstat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_madvise_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_madvise_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_mbind_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mbind_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_membarrier_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_membarrier_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_memfd_create_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_memfd_create_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_migrate_pages_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_migrate_pages_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mincore_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mincore_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mkdir_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mkdir_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mkdirat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mkdirat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mknod_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mknod_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mknodat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mknodat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mlock2_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_mlock2_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_mlock_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mlock_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mlockall_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_mlockall_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_mmap_pgoff_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mmap_pgoff_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_modify_ldt_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_modify_ldt_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mount_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mount_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_move_pages_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_move_pages_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_mprotect_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mprotect_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mq_getsetattr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mq_getsetattr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mq_notify_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mq_notify_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mq_open_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mq_open_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mq_timedreceive_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mq_timedreceive_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mq_timedsend_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mq_timedsend_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mq_unlink_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_mq_unlink_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_mremap_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_mremap_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_msync_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_msync_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_munlock_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_munlock_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_munlockall_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_munlockall_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_munmap_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_munmap_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_name_to_handle_at_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_name_to_handle_at_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_nanosleep_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_nanosleep_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_newfstat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_newfstat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_newlstat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_newlstat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_newstat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_newstat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_newuname_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_newuname_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_nice_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_nice_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_old_getrlimit_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_old_getrlimit_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_old_mmap_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_old_mmap_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_old_readdir_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_old_readdir_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_old_select_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_old_select_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_oldumount_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_oldumount_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_olduname_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_olduname_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_open_by_handle_at_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_open_by_handle_at_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_open_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_open_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_openat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_openat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_pause_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_pause_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_perf_event_open_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint], None]
on_sys_perf_event_open_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint], None]
on_sys_personality_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_personality_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_pipe2_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_pipe2_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_pipe_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_pipe_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_pivot_root_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_pivot_root_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_pkey_alloc_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_pkey_alloc_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_pkey_free_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_pkey_free_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_pkey_mprotect_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_pkey_mprotect_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_poll_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_poll_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_ppoll_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_ppoll_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_prctl_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_prctl_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_pread64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
on_sys_pread64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
on_sys_preadv2_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_preadv2_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_preadv_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_preadv_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_prlimit64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_prlimit64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_process_vm_readv_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_process_vm_readv_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_process_vm_writev_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_process_vm_writev_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_pselect6_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_pselect6_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_ptrace_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_ptrace_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_pwrite64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
on_sys_pwrite64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
on_sys_pwritev2_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_pwritev2_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_pwritev_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_pwritev_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_quotactl_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_quotactl_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_read_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_read_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_readahead_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_ulong, ctypes.c_uint], None]
on_sys_readahead_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_ulong, ctypes.c_uint], None]
on_sys_readlink_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_readlink_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_readlinkat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_readlinkat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_readv_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_readv_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_reboot_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_reboot_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_recvfrom_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_recvfrom_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_recvmmsg_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_recvmmsg_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_recvmsg_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_recvmsg_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_remap_file_pages_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_remap_file_pages_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_removexattr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_removexattr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_rename_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_rename_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_renameat2_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_renameat2_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_renameat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_renameat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_request_key_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_request_key_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_restart_syscall_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_restart_syscall_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_rmdir_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_rmdir_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_rt_sigaction_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_rt_sigaction_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_rt_sigpending_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_rt_sigpending_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_rt_sigprocmask_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_rt_sigprocmask_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_rt_sigqueueinfo_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint], None]
on_sys_rt_sigqueueinfo_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint], None]
on_sys_rt_sigreturn_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_rt_sigreturn_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_rt_sigsuspend_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_rt_sigsuspend_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_rt_sigtimedwait_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_rt_sigtimedwait_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_rt_tgsigqueueinfo_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint], None]
on_sys_rt_tgsigqueueinfo_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint], None]
on_sys_sched_get_priority_max_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_sched_get_priority_max_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_sched_get_priority_min_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_sched_get_priority_min_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_sched_getaffinity_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sched_getaffinity_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sched_getattr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sched_getattr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sched_getparam_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_sched_getparam_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_sched_getscheduler_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_sched_getscheduler_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_sched_rr_get_interval_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_sched_rr_get_interval_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_sched_setaffinity_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sched_setaffinity_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sched_setattr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sched_setattr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sched_setparam_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_sched_setparam_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_sched_setscheduler_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint], None]
on_sys_sched_setscheduler_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint], None]
on_sys_sched_yield_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_sched_yield_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_seccomp_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_seccomp_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_select_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_select_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sendfile64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sendfile64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sendfile_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sendfile_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sendmmsg_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sendmmsg_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sendmsg_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sendmsg_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sendto_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_sendto_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_set_mempolicy_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_set_mempolicy_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_set_robust_list_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_set_robust_list_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_set_thread_area_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_set_thread_area_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_set_tid_address_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_set_tid_address_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setdomainname_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_setdomainname_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_setfsgid16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setfsgid16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setfsgid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setfsgid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setfsuid16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setfsuid16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setfsuid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setfsuid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setgid16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setgid16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setgid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setgid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setgroups16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_setgroups16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_setgroups_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_setgroups_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_sethostname_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_sethostname_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_setitimer_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setitimer_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setns_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_setns_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_setpgid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_setpgid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_setpriority_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int], None]
on_sys_setpriority_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int], None]
on_sys_setregid16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setregid16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setregid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setregid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setresgid16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setresgid16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setresgid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setresgid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setresuid16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setresuid16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setresuid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setresuid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setreuid16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setreuid16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setreuid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setreuid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setrlimit_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setrlimit_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setsid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_setsid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_setsockopt_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_setsockopt_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_settimeofday_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_settimeofday_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_setuid16_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setuid16_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setuid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setuid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_setxattr_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_setxattr_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_sgetmask_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_sgetmask_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_shutdown_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_shutdown_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_sigaction_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sigaction_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sigaltstack_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sigaltstack_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_signal_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_signal_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_signalfd4_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_signalfd4_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_signalfd_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_signalfd_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sigpending_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_sigpending_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_sigprocmask_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sigprocmask_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sigreturn_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_sigreturn_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_sigsuspend_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint], None]
on_sys_sigsuspend_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint], None]
on_sys_socket_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int], None]
on_sys_socket_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int], None]
on_sys_socketcall_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_socketcall_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_socketpair_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint], None]
on_sys_socketpair_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint], None]
on_sys_splice_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_splice_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_ssetmask_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_ssetmask_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_stat64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_stat64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_stat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_stat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_statfs64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_statfs64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_statfs_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_statfs_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_statx_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_statx_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_stime_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_stime_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_swapoff_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_swapoff_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_swapon_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_swapon_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_symlink_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_symlink_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_symlinkat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_symlinkat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_sync_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_sync_file_range_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_uint], None]
on_sys_sync_file_range_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_uint], None]
on_sys_sync_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_syncfs_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_syncfs_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_sysctl_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_sysctl_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_sysfs_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sysfs_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_sysinfo_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_sysinfo_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_syslog_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_syslog_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_tee_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_tee_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_tgkill_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int], None]
on_sys_tgkill_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_int], None]
on_sys_time_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_time_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_timer_create_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_timer_create_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_timer_delete_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_timer_delete_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_timer_getoverrun_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_timer_getoverrun_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_timer_gettime_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_timer_gettime_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_timer_settime_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_timer_settime_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_timerfd_create_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_timerfd_create_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_timerfd_gettime_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_timerfd_gettime_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_timerfd_settime_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_timerfd_settime_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint], None]
on_sys_times_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_times_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_tkill_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_tkill_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_sys_truncate64_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
on_sys_truncate64_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
on_sys_truncate_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_truncate_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_umask_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_umask_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_umount_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_umount_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_uname_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_uname_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_unlink_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_unlink_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_unlinkat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_unlinkat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_unshare_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_unshare_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_uselib_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_uselib_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_userfaultfd_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_userfaultfd_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int], None]
on_sys_ustat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_ustat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_utime_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_utime_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_utimensat_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_utimensat_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_int], None]
on_sys_utimes_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_utimes_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_vfork_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_vfork_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_vhangup_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_vhangup_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
on_sys_vm86_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_vm86_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_vm86old_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_vm86old_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_sys_vmsplice_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_vmsplice_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_wait4_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_wait4_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_waitid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_waitid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_uint], None]
on_sys_waitpid_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_waitpid_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_int], None]
on_sys_write_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_write_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_writev_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_sys_writev_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint], None]
on_taint_change_t: Callable[[addr_struct, ctypes.c_ulong], None]
on_taint_prop_t: Callable[[addr_struct, addr_struct, ctypes.c_ulong], None]
on_task_change_t: Callable[[ctypes._Pointer[CPUState]], None]
on_thread_end_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_char], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_thread_start_t: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_char], ctypes.c_uint, ctypes.c_int, ctypes.c_int], None]
on_unknown_sys_enter_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
on_unknown_sys_return_t: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], None]
class panda_arg:
    argptr: ctypes._Pointer[ctypes.c_char]
    key: ctypes._Pointer[ctypes.c_char]
    value: ctypes._Pointer[ctypes.c_char]

class panda_arg_list:
    nargs: ctypes.c_int
    list: ctypes._Pointer[panda_arg]
    plugin_name: ctypes._Pointer[ctypes.c_char]

class panda_cb:
    before_block_exec_invalidate_opt: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], ctypes.c_bool]
    before_tcg_codegen: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    before_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    after_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes.c_ubyte], None]
    before_block_translate: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
    after_block_translate: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    after_cpu_exec_enter: Callable[[ctypes._Pointer[CPUState]], None]
    before_cpu_exec_exit: Callable[[ctypes._Pointer[CPUState], ctypes.c_bool], None]
    insn_translate: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_bool]
    insn_exec: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_int]
    after_insn_translate: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_bool]
    after_insn_exec: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_int]
    virt_mem_before_read: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
    virt_mem_before_write: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    phys_mem_before_read: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
    phys_mem_before_write: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    virt_mem_after_read: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    virt_mem_after_write: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    phys_mem_after_read: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    phys_mem_after_write: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    mmio_after_read: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ulong]], None]
    mmio_before_write: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ulong]], None]
    hd_read: Callable[[ctypes._Pointer[CPUState]], None]
    hd_write: Callable[[ctypes._Pointer[CPUState]], None]
    guest_hypercall: Callable[[ctypes._Pointer[CPUState]], ctypes.c_bool]
    monitor: Callable[[ctypes._Pointer[Monitor], ctypes._Pointer[ctypes.c_char]], ctypes.c_int]
    qmp: Callable[[ctypes._Pointer[ctypes.c_char], ctypes._Pointer[ctypes.c_char], ctypes._Pointer[ctypes._Pointer[ctypes.c_char]]], ctypes.c_bool]
    cpu_restore_state: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    before_loadvm: Callable[[], ctypes.c_int]
    asid_changed: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], ctypes.c_bool]
    replay_hd_transfer: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
    replay_before_dma: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_ubyte], ctypes.c_ulong, ctypes.c_ulong, ctypes.c_bool], None]
    replay_after_dma: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_ubyte], ctypes.c_ulong, ctypes.c_ulong, ctypes.c_bool], None]
    replay_handle_packet: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_ubyte], ctypes.c_ulong, ctypes.c_ubyte, ctypes.c_ulong], None]
    replay_net_transfer: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong], None]
    replay_serial_receive: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ubyte], None]
    replay_serial_read: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ubyte], None]
    replay_serial_send: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ubyte], None]
    replay_serial_write: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ubyte], None]
    after_machine_init: Callable[[ctypes._Pointer[CPUState]], None]
    after_loadvm: Callable[[ctypes._Pointer[CPUState]], None]
    top_loop: Callable[[ctypes._Pointer[CPUState]], None]
    during_machine_init: Callable[[ctypes._Pointer[MachineState]], None]
    main_loop_wait: Callable[[], None]
    pre_shutdown: Callable[[], None]
    unassigned_io_read: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ulong, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ulong]], ctypes.c_bool]
    unassigned_io_write: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong], ctypes.c_bool]
    before_handle_exception: Callable[[ctypes._Pointer[CPUState], ctypes.c_int], ctypes.c_int]
    before_handle_interrupt: Callable[[ctypes._Pointer[CPUState], ctypes.c_int], ctypes.c_int]
    start_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    end_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    cbaddr: Callable[[], None]

class panda_cb_list:
    entry: panda_cb_with_context
    owner: ctypes.c_void_p
    next: ctypes._Pointer[_panda_cb_list]
    prev: ctypes._Pointer[_panda_cb_list]
    enabled: ctypes.c_bool
    context: ctypes.c_void_p

class panda_cb_type(IntEnum):
    PANDA_CB_LAST: int = 51
    PANDA_CB_END_BLOCK_EXEC: int = 50
    PANDA_CB_START_BLOCK_EXEC: int = 49
    PANDA_CB_BEFORE_HANDLE_INTERRUPT: int = 48
    PANDA_CB_BEFORE_HANDLE_EXCEPTION: int = 47
    PANDA_CB_UNASSIGNED_IO_WRITE: int = 46
    PANDA_CB_UNASSIGNED_IO_READ: int = 45
    PANDA_CB_PRE_SHUTDOWN: int = 44
    PANDA_CB_MAIN_LOOP_WAIT: int = 43
    PANDA_CB_DURING_MACHINE_INIT: int = 42
    PANDA_CB_TOP_LOOP: int = 41
    PANDA_CB_AFTER_LOADVM: int = 40
    PANDA_CB_AFTER_MACHINE_INIT: int = 39
    PANDA_CB_BEFORE_CPU_EXEC_EXIT: int = 38
    PANDA_CB_AFTER_CPU_EXEC_ENTER: int = 37
    PANDA_CB_REPLAY_HANDLE_PACKET: int = 36
    PANDA_CB_REPLAY_AFTER_DMA: int = 35
    PANDA_CB_REPLAY_BEFORE_DMA: int = 34
    PANDA_CB_REPLAY_SERIAL_WRITE: int = 33
    PANDA_CB_REPLAY_SERIAL_SEND: int = 32
    PANDA_CB_REPLAY_SERIAL_READ: int = 31
    PANDA_CB_REPLAY_SERIAL_RECEIVE: int = 30
    PANDA_CB_REPLAY_NET_TRANSFER: int = 29
    PANDA_CB_REPLAY_HD_TRANSFER: int = 28
    PANDA_CB_ASID_CHANGED: int = 27
    PANDA_CB_BEFORE_LOADVM: int = 26
    PANDA_CB_CPU_RESTORE_STATE: int = 25
    PANDA_CB_QMP: int = 24
    PANDA_CB_MONITOR: int = 23
    PANDA_CB_GUEST_HYPERCALL: int = 22
    PANDA_CB_HD_WRITE: int = 21
    PANDA_CB_HD_READ: int = 20
    PANDA_CB_MMIO_BEFORE_WRITE: int = 19
    PANDA_CB_MMIO_AFTER_READ: int = 18
    PANDA_CB_PHYS_MEM_AFTER_WRITE: int = 17
    PANDA_CB_PHYS_MEM_AFTER_READ: int = 16
    PANDA_CB_VIRT_MEM_AFTER_WRITE: int = 15
    PANDA_CB_VIRT_MEM_AFTER_READ: int = 14
    PANDA_CB_PHYS_MEM_BEFORE_WRITE: int = 13
    PANDA_CB_PHYS_MEM_BEFORE_READ: int = 12
    PANDA_CB_VIRT_MEM_BEFORE_WRITE: int = 11
    PANDA_CB_VIRT_MEM_BEFORE_READ: int = 10
    PANDA_CB_AFTER_INSN_EXEC: int = 9
    PANDA_CB_AFTER_INSN_TRANSLATE: int = 8
    PANDA_CB_INSN_EXEC: int = 7
    PANDA_CB_INSN_TRANSLATE: int = 6
    PANDA_CB_AFTER_BLOCK_EXEC: int = 5
    PANDA_CB_BEFORE_BLOCK_EXEC: int = 4
    PANDA_CB_BEFORE_TCG_CODEGEN: int = 3
    PANDA_CB_BEFORE_BLOCK_EXEC_INVALIDATE_OPT: int = 2
    PANDA_CB_AFTER_BLOCK_TRANSLATE: int = 1
    PANDA_CB_BEFORE_BLOCK_TRANSLATE: int = 0

class panda_cb_with_context:
    before_block_exec_invalidate_opt: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], ctypes.c_bool]
    before_tcg_codegen: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    before_block_exec: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    after_block_exec: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes.c_ubyte], None]
    before_block_translate: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint], None]
    after_block_translate: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    after_cpu_exec_enter: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState]], None]
    before_cpu_exec_exit: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_bool], None]
    insn_translate: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_bool]
    insn_exec: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_int]
    after_insn_translate: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_bool]
    after_insn_exec: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_int]
    virt_mem_before_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
    virt_mem_before_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    phys_mem_before_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
    phys_mem_before_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    virt_mem_after_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    virt_mem_after_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    phys_mem_after_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    phys_mem_after_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    mmio_after_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ulong]], None]
    mmio_before_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ulong]], None]
    hd_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState]], None]
    hd_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState]], None]
    guest_hypercall: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState]], ctypes.c_bool]
    monitor: Callable[[ctypes.c_void_p, ctypes._Pointer[Monitor], ctypes._Pointer[ctypes.c_char]], ctypes.c_int]
    qmp: Callable[[ctypes.c_void_p, ctypes._Pointer[ctypes.c_char], ctypes._Pointer[ctypes.c_char], ctypes._Pointer[ctypes._Pointer[ctypes.c_char]]], ctypes.c_bool]
    cpu_restore_state: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    before_loadvm: Callable[[ctypes.c_void_p], ctypes.c_int]
    asid_changed: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], ctypes.c_bool]
    replay_hd_transfer: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
    replay_before_dma: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_ubyte], ctypes.c_ulong, ctypes.c_ulong, ctypes.c_bool], None]
    replay_after_dma: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_ubyte], ctypes.c_ulong, ctypes.c_ulong, ctypes.c_bool], None]
    replay_handle_packet: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_ubyte], ctypes.c_ulong, ctypes.c_ubyte, ctypes.c_ulong], None]
    replay_net_transfer: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong], None]
    replay_serial_receive: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ubyte], None]
    replay_serial_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ubyte], None]
    replay_serial_send: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ubyte], None]
    replay_serial_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ubyte], None]
    after_machine_init: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState]], None]
    after_loadvm: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState]], None]
    top_loop: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState]], None]
    during_machine_init: Callable[[ctypes.c_void_p, ctypes._Pointer[MachineState]], None]
    main_loop_wait: Callable[[ctypes.c_void_p], None]
    pre_shutdown: Callable[[ctypes.c_void_p], None]
    unassigned_io_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ulong, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ulong]], ctypes.c_bool]
    unassigned_io_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong], ctypes.c_bool]
    before_handle_exception: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_int], ctypes.c_int]
    before_handle_interrupt: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_int], ctypes.c_int]
    start_block_exec: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    end_block_exec: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    cbaddr: Callable[[], None]

class panda_plugin:
    name: ctypes._Pointer[ctypes.c_char]
    plugin: ctypes.c_void_p
    unload: ctypes.c_bool
    exported_symbols: ctypes.c_bool

powerpc_excp_t: ctypes.c_uint
powerpc_input_t: ctypes.c_uint
powerpc_mmu_t: ctypes.c_uint
ppc_avr_t: ctypes.Array[ctypes.c_ubyte]
ppc_tlb_t: ctypes.Array[ctypes.c_ubyte]
pthread_cond_t: ctypes.Array[ctypes.c_ubyte]
pthread_mutex_t: ctypes.Array[ctypes.c_ubyte]
pthread_t: ctypes.c_ulong
class qemu_work_item:
    next: ctypes._Pointer[qemu_work_item]
    func: ctypes.c_void_p
    data: ctypes.c_ulong
    free: ctypes.c_bool
    exclusive: ctypes.c_bool
    done: ctypes.c_bool

ram_addr_t: ctypes.c_ulong
class rcu_head:
    next: ctypes._Pointer[rcu_head]
    func: Callable[[ctypes._Pointer[rcu_head]], None]

run_on_cpu_data: ctypes.c_ulong
run_on_cpu_func: ctypes.c_void_p
sigjmp_buf: ctypes.Array[ctypes.c_ubyte]
class subregions:
    tqh_first: ctypes._Pointer[MemoryRegion]
    tqh_last: ctypes._Pointer[ctypes._Pointer[MemoryRegion]]

class syscall_argtype_t(IntEnum):
    SYSCALL_ARG_ARR: int = 49
    SYSCALL_ARG_STRUCT: int = 48
    SYSCALL_ARG_STR_PTR: int = 34
    SYSCALL_ARG_STRUCT_PTR: int = 33
    SYSCALL_ARG_BUF_PTR: int = 32
    SYSCALL_ARG_S16: int = 18
    SYSCALL_ARG_S32: int = 17
    SYSCALL_ARG_S64: int = 16
    SYSCALL_ARG_U16: int = 2
    SYSCALL_ARG_U32: int = 1
    SYSCALL_ARG_U64: int = 0

class syscall_ctx_t:
    no: ctypes.c_int
    asid: ctypes.c_uint
    retaddr: ctypes.c_uint
    args: ctypes.Array[ctypes.Array[ctypes.c_ubyte]]

class syscall_info_t:
    no: ctypes.c_int
    name: ctypes._Pointer[ctypes.c_char]
    nargs: ctypes.c_int
    argt: ctypes._Pointer[syscall_argtype_t]
    argsz: ctypes._Pointer[ctypes.c_ubyte]
    argn: ctypes._Pointer[ctypes._Pointer[ctypes.c_char]]
    argtn: ctypes._Pointer[ctypes._Pointer[ctypes.c_char]]
    noreturn: ctypes.c_bool

class syscall_meta_t:
    max: ctypes.c_uint
    max_generic: ctypes.c_uint
    max_args: ctypes.c_uint

target_long: ctypes.c_int
target_pid_t: ctypes.c_int
target_ptr_t: ctypes.c_uint
target_ulong: ctypes.c_uint
tb_page_addr_t: ctypes.c_ulong
vaddr: ctypes.c_ulong
class watchpoints_head:
    tqh_first: ctypes._Pointer[CPUWatchpoint]
    tqh_last: ctypes._Pointer[ctypes._Pointer[CPUWatchpoint]]

class AccelState:
    parent_obj: Object

class AddrRange:
    start: ctypes.Array[ctypes.c_ubyte]
    size: ctypes.Array[ctypes.c_ubyte]

class AddressSpace:
    rcu: rcu_head
    name: ctypes._Pointer[ctypes.c_char]
    root: ctypes._Pointer[MemoryRegion]
    ref_count: ctypes.c_int
    malloced: ctypes.c_bool
    current_map: ctypes._Pointer[FlatView]
    ioeventfd_nb: ctypes.c_int
    ioeventfds: ctypes._Pointer[MemoryRegionIoeventfd]
    dispatch: ctypes._Pointer[AddressSpaceDispatch]
    next_dispatch: ctypes._Pointer[AddressSpaceDispatch]
    dispatch_listener: MemoryListener
    listeners: memory_listeners_as
    class internal_7:
        tqe_next: ctypes._Pointer[AddressSpace]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[AddressSpace]]

    address_spaces_link: internal_7

class AddressSpaceDispatch:
    pass

class BNDCSReg:
    cfgu: ctypes.c_ulong
    sts: ctypes.c_ulong

class BNDReg:
    lb: ctypes.c_ulong
    ub: ctypes.c_ulong

class BusChild:
    pass

class BusState:
    obj: Object
    parent: ctypes._Pointer[DeviceState]
    name: ctypes._Pointer[ctypes.c_char]
    hotplug_handler: ctypes._Pointer[HotplugHandler]
    max_index: ctypes.c_int
    realized: ctypes.c_bool
    children: ChildrenHead
    class internal_21:
        le_next: ctypes._Pointer[BusState]
        le_prev: ctypes._Pointer[ctypes._Pointer[BusState]]

    sibling: internal_21

class CPUAddressSpace:
    cpu: ctypes._Pointer[CPUState]
    memory_dispatch: ctypes._Pointer[AddressSpaceDispatch]
    tcg_as_listener: MemoryListener
setattr(CPUAddressSpace, "as", ctypes._Pointer[AddressSpace]())

class CPUBreakpoint:
    pc: ctypes.c_ulong
    rr_instr_count: ctypes.c_ulong
    flags: ctypes.c_int
    entry: CPUBreakpoint_qtailq

class CPUIOTLBEntry:
    addr: ctypes.c_ulong
    attrs: MemTxAttrs

class CPUState:
    parent_obj: DeviceState
    nr_cores: ctypes.c_int
    nr_threads: ctypes.c_int
    numa_node: ctypes.c_int
    thread: ctypes._Pointer[QemuThread]
    thread_id: ctypes.c_int
    host_tid: ctypes.c_uint
    running: ctypes.c_bool
    has_waiter: ctypes.c_bool
    halt_cond: ctypes._Pointer[QemuCond]
    thread_kicked: ctypes.c_bool
    created: ctypes.c_bool
    stop: ctypes.c_bool
    stopped: ctypes.c_bool
    unplug: ctypes.c_bool
    crash_occurred: ctypes.c_bool
    exit_request: ctypes.c_bool
    interrupt_request: ctypes.c_uint
    singlestep_enabled: ctypes.c_int
    icount_budget: ctypes.c_long
    icount_extra: ctypes.c_long
    jmp_env: ctypes.Array[ctypes.c_ubyte]
    work_mutex: QemuMutex
    queued_work_first: ctypes._Pointer[qemu_work_item]
    queued_work_last: ctypes._Pointer[qemu_work_item]
    cpu_ases: ctypes._Pointer[CPUAddressSpace]
    num_ases: ctypes.c_int
    memory: ctypes._Pointer[MemoryRegion]
    env_ptr: ctypes._Pointer[CPUX86State]
    tb_jmp_cache: ctypes.Array[ctypes._Pointer[TranslationBlock]]
    gdb_regs: ctypes._Pointer[GDBRegisterState]
    gdb_num_regs: ctypes.c_int
    gdb_num_g_regs: ctypes.c_int
    class internal_23:
        tqe_next: ctypes._Pointer[CPUState]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[CPUState]]

    node: internal_23
    breakpoints: breakpoints_head
    watchpoints: watchpoints_head
    watchpoint_hit: ctypes._Pointer[CPUWatchpoint]
    watchpoints_disabled: ctypes.c_bool
    opaque: ctypes.c_void_p
    mem_io_pc: ctypes.c_ulong
    mem_io_vaddr: ctypes.c_ulong
    kvm_fd: ctypes.c_int
    kvm_vcpu_dirty: ctypes.c_bool
    kvm_state: ctypes._Pointer[KVMState]
    kvm_run: ctypes._Pointer[kvm_run]
    trace_dstate: ctypes._Pointer[ctypes.c_ulong]
    cpu_index: ctypes.c_int
    halted: ctypes.c_uint
    class internal_24:
        u32: ctypes.c_uint
        u16: icount_decr_u16

    icount_decr: internal_24
    can_do_io: ctypes.c_uint
    exception_index: ctypes.c_int
    rr_guest_instr_count: ctypes.c_ulong
    panda_guest_pc: ctypes.c_ulong
    reverse_flags: ctypes.c_ubyte
    last_gdb_instr: ctypes.c_ulong
    last_bp_hit_instr: ctypes.c_ulong
    temp_rr_bp_instr: ctypes.c_ulong
    throttle_thread_scheduled: ctypes.c_bool
    tcg_exit_req: ctypes.c_uint
    hax_vcpu_dirty: ctypes.c_bool
    hax_vcpu: ctypes._Pointer[hax_vcpu_state]
    pending_tlb_flush: ctypes.c_ushort
setattr(CPUState, "as", ctypes._Pointer[AddressSpace]())

class CPUTLBEntry:
    addr_read: ctypes.c_uint
    addr_write: ctypes.c_uint
    addr_code: ctypes.c_uint
    addend: ctypes.c_ulong
    dummy: ctypes.Array[ctypes.c_ubyte]

class CPUWatchpoint:
    virtaddr: ctypes.c_ulong
    len: ctypes.c_ulong
    hitaddr: ctypes.c_ulong
    hitattrs: MemTxAttrs
    flags: ctypes.c_int
    class internal_6:
        tqe_next: ctypes._Pointer[CPUWatchpoint]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[CPUWatchpoint]]

    entry: internal_6

class CPUX86State:
    regs: ctypes.Array[ctypes.c_uint]
    eip: ctypes.c_uint
    eflags: ctypes.c_uint
    cc_dst: ctypes.c_uint
    cc_src: ctypes.c_uint
    cc_src2: ctypes.c_uint
    cc_op: ctypes.c_uint
    df: ctypes.c_int
    hflags: ctypes.c_uint
    hflags2: ctypes.c_uint
    segs: ctypes.Array[SegmentCache]
    ldt: SegmentCache
    tr: SegmentCache
    gdt: SegmentCache
    idt: SegmentCache
    cr: ctypes.Array[ctypes.c_uint]
    a20_mask: ctypes.c_int
    bnd_regs: ctypes.Array[BNDReg]
    bndcs_regs: BNDCSReg
    msr_bndcfgs: ctypes.c_ulong
    efer: ctypes.c_ulong
    fpstt: ctypes.c_uint
    fpus: ctypes.c_ushort
    fpuc: ctypes.c_ushort
    fptags: ctypes.Array[ctypes.c_ubyte]
    fpregs: ctypes.Array[ctypes.Array[ctypes.c_ubyte]]
    fpop: ctypes.c_ushort
    fpip: ctypes.c_ulong
    fpdp: ctypes.c_ulong
    fp_status: float_status
    ft0: floatx80
    mmx_status: float_status
    sse_status: float_status
    mxcsr: ctypes.c_uint
    xmm_regs: ctypes.Array[ctypes.Array[ctypes.c_ubyte]]
    xmm_t0: ctypes.Array[ctypes.c_ubyte]
    mmx_t0: ctypes.Array[ctypes.c_ubyte]
    opmask_regs: ctypes.Array[ctypes.c_ulong]
    sysenter_cs: ctypes.c_uint
    sysenter_esp: ctypes.c_uint
    sysenter_eip: ctypes.c_uint
    star: ctypes.c_ulong
    vm_hsave: ctypes.c_ulong
    tsc: ctypes.c_ulong
    tsc_adjust: ctypes.c_ulong
    tsc_deadline: ctypes.c_ulong
    tsc_aux: ctypes.c_ulong
    xcr0: ctypes.c_ulong
    mcg_status: ctypes.c_ulong
    msr_ia32_misc_enable: ctypes.c_ulong
    msr_ia32_feature_control: ctypes.c_ulong
    msr_fixed_ctr_ctrl: ctypes.c_ulong
    msr_global_ctrl: ctypes.c_ulong
    msr_global_status: ctypes.c_ulong
    msr_global_ovf_ctrl: ctypes.c_ulong
    msr_fixed_counters: ctypes.Array[ctypes.c_ulong]
    msr_gp_counters: ctypes.Array[ctypes.c_ulong]
    msr_gp_evtsel: ctypes.Array[ctypes.c_ulong]
    pat: ctypes.c_ulong
    smbase: ctypes.c_uint
    pkru: ctypes.c_uint
    system_time_msr: ctypes.c_ulong
    wall_clock_msr: ctypes.c_ulong
    steal_time_msr: ctypes.c_ulong
    async_pf_en_msr: ctypes.c_ulong
    pv_eoi_en_msr: ctypes.c_ulong
    msr_hv_hypercall: ctypes.c_ulong
    msr_hv_guest_os_id: ctypes.c_ulong
    msr_hv_vapic: ctypes.c_ulong
    msr_hv_tsc: ctypes.c_ulong
    msr_hv_crash_params: ctypes.Array[ctypes.c_ulong]
    msr_hv_runtime: ctypes.c_ulong
    msr_hv_synic_control: ctypes.c_ulong
    msr_hv_synic_version: ctypes.c_ulong
    msr_hv_synic_evt_page: ctypes.c_ulong
    msr_hv_synic_msg_page: ctypes.c_ulong
    msr_hv_synic_sint: ctypes.Array[ctypes.c_ulong]
    msr_hv_stimer_config: ctypes.Array[ctypes.c_ulong]
    msr_hv_stimer_count: ctypes.Array[ctypes.c_ulong]
    error_code: ctypes.c_int
    exception_is_int: ctypes.c_int
    exception_next_eip: ctypes.c_uint
    dr: ctypes.Array[ctypes.c_uint]
    cpu_breakpoint: ctypes.Array[ctypes._Pointer[CPUBreakpoint]]
    cpu_watchpoint: ctypes.Array[ctypes._Pointer[CPUWatchpoint]]
    old_exception: ctypes.c_int
    vm_vmcb: ctypes.c_ulong
    tsc_offset: ctypes.c_ulong
    intercept: ctypes.c_ulong
    intercept_cr_read: ctypes.c_ushort
    intercept_cr_write: ctypes.c_ushort
    intercept_dr_read: ctypes.c_ushort
    intercept_dr_write: ctypes.c_ushort
    intercept_exceptions: ctypes.c_uint
    v_tpr: ctypes.c_ubyte
    nmi_injected: ctypes.c_ubyte
    nmi_pending: ctypes.c_ubyte
    tlb_table: ctypes.Array[ctypes.Array[CPUTLBEntry]]
    tlb_v_table: ctypes.Array[ctypes.Array[CPUTLBEntry]]
    iotlb: ctypes.Array[ctypes.Array[CPUIOTLBEntry]]
    iotlb_v: ctypes.Array[ctypes.Array[CPUIOTLBEntry]]
    tlb_flush_addr: ctypes.c_uint
    tlb_flush_mask: ctypes.c_uint
    vtlb_index: ctypes.c_uint
    cpuid_min_level: ctypes.c_uint
    cpuid_min_xlevel: ctypes.c_uint
    cpuid_min_xlevel2: ctypes.c_uint
    cpuid_max_level: ctypes.c_uint
    cpuid_max_xlevel: ctypes.c_uint
    cpuid_max_xlevel2: ctypes.c_uint
    cpuid_level: ctypes.c_uint
    cpuid_xlevel: ctypes.c_uint
    cpuid_xlevel2: ctypes.c_uint
    cpuid_vendor1: ctypes.c_uint
    cpuid_vendor2: ctypes.c_uint
    cpuid_vendor3: ctypes.c_uint
    cpuid_version: ctypes.c_uint
    features: ctypes.Array[ctypes.c_uint]
    user_features: ctypes.Array[ctypes.c_uint]
    cpuid_model: ctypes.Array[ctypes.c_uint]
    mtrr_fixed: ctypes.Array[ctypes.c_ulong]
    mtrr_deftype: ctypes.c_ulong
    mtrr_var: ctypes.Array[MTRRVar]
    mp_state: ctypes.c_uint
    exception_injected: ctypes.c_int
    interrupt_injected: ctypes.c_int
    soft_interrupt: ctypes.c_ubyte
    has_error_code: ctypes.c_ubyte
    sipi_vector: ctypes.c_uint
    tsc_valid: ctypes.c_bool
    tsc_khz: ctypes.c_long
    user_tsc_khz: ctypes.c_long
    kvm_xsave_buf: ctypes.c_void_p
    mcg_cap: ctypes.c_ulong
    mcg_ctl: ctypes.c_ulong
    mcg_ext_ctl: ctypes.c_ulong
    mce_banks: ctypes.Array[ctypes.c_ulong]
    xstate_bv: ctypes.c_ulong
    fpus_vmstate: ctypes.c_ushort
    fptag_vmstate: ctypes.c_ushort
    fpregs_format_vmstate: ctypes.c_ushort
    xss: ctypes.c_ulong
    tpr_access_type: TPRAccess

class CharBackend:
    chr: ctypes._Pointer[Chardev]
    chr_event: Callable[[ctypes.c_void_p, ctypes.c_int], None]
    chr_can_read: Callable[[ctypes.c_void_p], ctypes.c_int]
    chr_read: Callable[[ctypes.c_void_p, ctypes._Pointer[ctypes.c_ubyte], ctypes.c_int], None]
    opaque: ctypes.c_void_p
    tag: ctypes.c_int
    fe_open: ctypes.c_int

class Chardev:
    parent_obj: Object
    chr_write_lock: QemuMutex
    be: ctypes._Pointer[CharBackend]
    label: ctypes._Pointer[ctypes.c_char]
    filename: ctypes._Pointer[ctypes.c_char]
    logfd: ctypes.c_int
    be_open: ctypes.c_int
    fd_in_tag: ctypes.c_uint
    features: ctypes.Array[ctypes.c_ulong]
    class internal_18:
        tqe_next: ctypes._Pointer[Chardev]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[Chardev]]

    next: internal_18

class ChildrenHead:
    tqh_first: ctypes._Pointer[BusChild]
    tqh_last: ctypes._Pointer[ctypes._Pointer[BusChild]]

class CoalescedMemoryRange:
    pass

class CosiFile:
    addr: ctypes.c_uint
    file_struct: File
    name: ctypes._Pointer[String]
    fd: ctypes.c_uint

class CosiFiles:
    pass

class CosiMappings:
    modules: ctypes._Pointer[Vec_CosiModule]

class CosiModule:
    modd: ctypes.c_uint
    base: ctypes.c_uint
    size: ctypes.c_uint
    vma: VmAreaStruct
    file: ctypes._Pointer[String]
    name: ctypes._Pointer[String]

class CosiProc:
    addr: ctypes.c_uint
    task: TaskStruct
    name: ctypes._Pointer[String]
    ppid: ctypes.c_uint
    mm: ctypes._Pointer[MmStruct]
    asid: ctypes.c_uint
    taskd: ctypes.c_uint

class CosiThread:
    tid: ctypes.c_uint
    pid: ctypes.c_uint

class DeviceState:
    parent_obj: Object
    id: ctypes._Pointer[ctypes.c_char]
    realized: ctypes.c_bool
    pending_deleted_event: ctypes.c_bool
    opts: ctypes._Pointer[QemuOpts]
    hotplugged: ctypes.c_int
    parent_bus: ctypes._Pointer[BusState]
    class internal_16:
        lh_first: ctypes._Pointer[NamedGPIOList]

    gpios: internal_16
    class internal_17:
        lh_first: ctypes._Pointer[BusState]

    child_bus: internal_17
    num_child_bus: ctypes.c_int
    instance_id_alias: ctypes.c_int
    alias_required_for_version: ctypes.c_int

class EventNotifier:
    rfd: ctypes.c_int
    wfd: ctypes.c_int

class File:
    f_path: Path
    f_pos: ctypes.c_uint

class FlatView:
    pass

class GDBRegisterState:
    base_reg: ctypes.c_int
    num_regs: ctypes.c_int
    get_reg: ctypes.c_int
    set_reg: ctypes.c_int
    xml: ctypes._Pointer[ctypes.c_char]
    next: ctypes._Pointer[GDBRegisterState]

class GHashTable:
    pass

class HotplugHandler:
    Parent: Object

class IOMMUNotifier:
    pass

class IOMMUTLBEntry:
    target_as: ctypes._Pointer[AddressSpace]
    iova: ctypes.c_ulong
    translated_addr: ctypes.c_ulong
    addr_mask: ctypes.c_ulong
    perm: IOMMUAccessFlags

class KVMState:
    pass

class ListHead:
    next: ctypes.c_uint
    prev: ctypes.c_uint

class Location:
    num: ctypes.c_int
    ptr: ctypes.c_void_p
    prev: ctypes._Pointer[Location]

class MachineState:
    parent_obj: Object
    sysbus_notifier: Notifier
    accel: ctypes._Pointer[ctypes.c_char]
    kernel_irqchip_allowed: ctypes.c_bool
    kernel_irqchip_required: ctypes.c_bool
    kernel_irqchip_split: ctypes.c_bool
    kvm_shadow_mem: ctypes.c_int
    dtb: ctypes._Pointer[ctypes.c_char]
    dumpdtb: ctypes._Pointer[ctypes.c_char]
    phandle_start: ctypes.c_int
    dt_compatible: ctypes._Pointer[ctypes.c_char]
    dump_guest_core: ctypes.c_bool
    mem_merge: ctypes.c_bool
    usb: ctypes.c_bool
    usb_disabled: ctypes.c_bool
    igd_gfx_passthru: ctypes.c_bool
    firmware: ctypes._Pointer[ctypes.c_char]
    iommu: ctypes.c_bool
    suppress_vmdesc: ctypes.c_bool
    enforce_config_section: ctypes.c_bool
    enable_graphics: ctypes.c_bool
    board_id: ctypes.c_int
    mem_map_str: ctypes._Pointer[ctypes.c_char]
    ram_size: ctypes.c_ulong
    maxram_size: ctypes.c_ulong
    ram_slots: ctypes.c_ulong
    boot_order: ctypes._Pointer[ctypes.c_char]
    kernel_filename: ctypes._Pointer[ctypes.c_char]
    kernel_cmdline: ctypes._Pointer[ctypes.c_char]
    initrd_filename: ctypes._Pointer[ctypes.c_char]
    cpu_model: ctypes._Pointer[ctypes.c_char]
    accelerator: ctypes._Pointer[AccelState]
    possible_cpus: ctypes._Pointer[ctypes.c_ulong]

class MemTxAttrs:
    unspecified: ctypes.c_uint
    secure: ctypes.c_uint
    user: ctypes.c_uint
    requester_id: ctypes.c_uint

class MemoryListener:
    begin: Callable[[ctypes._Pointer[MemoryListener]], None]
    commit: Callable[[ctypes._Pointer[MemoryListener]], None]
    region_add: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection]], None]
    region_del: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection]], None]
    region_nop: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection]], None]
    log_start: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection], ctypes.c_int, ctypes.c_int], None]
    log_stop: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection], ctypes.c_int, ctypes.c_int], None]
    log_sync: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection]], None]
    log_global_start: Callable[[ctypes._Pointer[MemoryListener]], None]
    log_global_stop: Callable[[ctypes._Pointer[MemoryListener]], None]
    eventfd_add: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection], ctypes.c_bool, ctypes.c_ulong, ctypes._Pointer[EventNotifier]], None]
    eventfd_del: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection], ctypes.c_bool, ctypes.c_ulong, ctypes._Pointer[EventNotifier]], None]
    coalesced_mmio_add: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection], ctypes.c_ulong, ctypes.c_ulong], None]
    coalesced_mmio_del: Callable[[ctypes._Pointer[MemoryListener], ctypes._Pointer[MemoryRegionSection], ctypes.c_ulong, ctypes.c_ulong], None]
    priority: ctypes.c_uint
    address_space: ctypes._Pointer[AddressSpace]
    class internal_13:
        tqe_next: ctypes._Pointer[MemoryListener]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[MemoryListener]]

    link: internal_13
    class internal_14:
        tqe_next: ctypes._Pointer[MemoryListener]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[MemoryListener]]

    link_as: internal_14

class MemoryRegion:
    parent_obj: Object
    romd_mode: ctypes.c_bool
    ram: ctypes.c_bool
    subpage: ctypes.c_bool
    readonly: ctypes.c_bool
    rom_device: ctypes.c_bool
    flush_coalesced_mmio: ctypes.c_bool
    global_locking: ctypes.c_bool
    dirty_log_mask: ctypes.c_ubyte
    ram_block: ctypes._Pointer[RAMBlock]
    owner: ctypes._Pointer[Object]
    iommu_ops: ctypes._Pointer[MemoryRegionIOMMUOps]
    ops: ctypes._Pointer[MemoryRegionOps]
    opaque: ctypes.c_void_p
    container: ctypes._Pointer[MemoryRegion]
    size: ctypes.Array[ctypes.c_ubyte]
    addr: ctypes.c_ulong
    destructor: Callable[[ctypes._Pointer[MemoryRegion]], None]
    align: ctypes.c_ulong
    terminates: ctypes.c_bool
    ram_device: ctypes.c_bool
    enabled: ctypes.c_bool
    warning_printed: ctypes.c_bool
    vga_logging_count: ctypes.c_ubyte
    alias: ctypes._Pointer[MemoryRegion]
    alias_offset: ctypes.c_ulong
    priority: ctypes.c_int
    subregions: subregions
    class internal_11:
        tqe_next: ctypes._Pointer[MemoryRegion]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[MemoryRegion]]

    subregions_link: internal_11
    coalesced: coalesced_ranges
    name: ctypes._Pointer[ctypes.c_char]
    ioeventfd_nb: ctypes.c_uint
    ioeventfds: ctypes._Pointer[MemoryRegionIoeventfd]
    class internal_12:
        lh_first: ctypes._Pointer[IOMMUNotifier]

    iommu_notify: internal_12
    iommu_notify_flags: IOMMUNotifierFlag

class MemoryRegionIOMMUOps:
    translate: Callable[[ctypes._Pointer[MemoryRegion], ctypes.c_ulong, ctypes.c_bool], IOMMUTLBEntry]
    get_min_page_size: Callable[[ctypes._Pointer[MemoryRegion]], ctypes.c_ulong]
    notify_flag_changed: Callable[[ctypes._Pointer[MemoryRegion], IOMMUNotifierFlag, IOMMUNotifierFlag], None]

class MemoryRegionIoeventfd:
    addr: AddrRange
    match_data: ctypes.c_bool
    data: ctypes.c_ulong
    e: ctypes._Pointer[EventNotifier]

class MemoryRegionMmio:
    read: ctypes.Array[Callable[[ctypes.c_void_p, ctypes.c_ulong], ctypes.c_uint]]
    write: ctypes.Array[Callable[[ctypes.c_void_p, ctypes.c_ulong, ctypes.c_uint], None]]

class MemoryRegionOps:
    read: Callable[[ctypes.c_void_p, ctypes.c_ulong, ctypes.c_uint], ctypes.c_ulong]
    write: Callable[[ctypes.c_void_p, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_uint], None]
    read_with_attrs: Callable[[ctypes.c_void_p, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ulong], ctypes.c_uint, MemTxAttrs], ctypes.c_ulong]
    write_with_attrs: Callable[[ctypes.c_void_p, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_uint, MemTxAttrs], ctypes.c_ulong]
    endianness: device_endian
    class internal_9:
        min_access_size: ctypes.c_uint
        max_access_size: ctypes.c_uint
        unaligned: ctypes.c_bool
        accepts: Callable[[ctypes.c_void_p, ctypes.c_ulong, ctypes.c_uint, ctypes.c_bool], ctypes.c_bool]

    valid: internal_9
    class internal_10:
        min_access_size: ctypes.c_uint
        max_access_size: ctypes.c_uint
        unaligned: ctypes.c_bool

    impl: internal_10
    old_mmio: MemoryRegionMmio

class MemoryRegionSection:
    mr: ctypes._Pointer[MemoryRegion]
    address_space: ctypes._Pointer[AddressSpace]
    offset_within_region: ctypes.c_ulong
    size: ctypes.Array[ctypes.c_ubyte]
    offset_within_address_space: ctypes.c_ulong
    readonly: ctypes.c_bool

class MmStruct:
    pgd: ctypes.c_uint
    arg_start: ctypes.c_uint
    start_brk: ctypes.c_uint
    brk: ctypes.c_uint
    start_stack: ctypes.c_uint
    mmap: ctypes.c_uint

class Monitor:
    chr: CharBackend
    reset_seen: ctypes.c_int
    flags: ctypes.c_int
    suspend_cnt: ctypes.c_int
    skip_flush: ctypes.c_bool
    out_lock: QemuMutex
    outbuf: ctypes._Pointer[QString]
    out_watch: ctypes.c_uint
    mux_out: ctypes.c_int
    rs: ctypes._Pointer[ReadLineState]
    qmp: ctypes.Array[ctypes.c_ubyte]
    mon_cpu: ctypes._Pointer[CPUState]
    password_completion_cb: Callable[[ctypes.c_void_p, ctypes.c_int], None]
    password_opaque: ctypes.c_void_p
    cmd_table: ctypes._Pointer[ctypes.Array[ctypes.c_ubyte]]
    class internal_19:
        lh_first: ctypes._Pointer[mon_fd_t]

    fds: internal_19
    class internal_20:
        le_next: ctypes._Pointer[Monitor]
        le_prev: ctypes._Pointer[ctypes._Pointer[Monitor]]

    entry: internal_20

class NamedGPIOList:
    pass

class Notifier:
    notify: Callable[[ctypes._Pointer[Notifier], ctypes.c_void_p], None]
    class internal_3:
        le_next: ctypes._Pointer[Notifier]
        le_prev: ctypes._Pointer[ctypes._Pointer[Notifier]]

    node: internal_3

class Object:
    klass: ctypes.c_void_p
    free: ctypes.c_void_p
    properties: ctypes.c_void_p
    ref: ctypes.c_uint
    parent: ctypes.c_void_p

class Path:
    dentry: ctypes.c_uint
    mnt: ctypes.c_uint

class QObject:
    type: ctypes.c_uint
    refcnt: ctypes.c_ulong

class QString:
    base: QObject
    string: ctypes._Pointer[ctypes.c_char]
    length: ctypes.c_ulong
    capacity: ctypes.c_ulong

class QemuCond:
    cond: ctypes.Array[ctypes.c_ubyte]

class QemuMutex:
    lock: ctypes.Array[ctypes.c_ubyte]

class QemuOpt:
    pass

class QemuOptDesc:
    name: ctypes._Pointer[ctypes.c_char]
    type: QemuOptType
    help: ctypes._Pointer[ctypes.c_char]
    def_value_str: ctypes._Pointer[ctypes.c_char]

class QemuOptHead:
    tqh_first: ctypes._Pointer[QemuOpt]
    tqh_last: ctypes._Pointer[ctypes._Pointer[QemuOpt]]

class QemuOpts:
    id: ctypes._Pointer[ctypes.c_char]
    list: ctypes._Pointer[QemuOptsList]
    loc: Location
    head: QemuOptHead
    class internal_15:
        tqe_next: ctypes._Pointer[QemuOpts]
        tqe_prev: ctypes._Pointer[ctypes._Pointer[QemuOpts]]

    next: internal_15

class QemuOptsList:
    name: ctypes._Pointer[ctypes.c_char]
    implied_opt_name: ctypes._Pointer[ctypes.c_char]
    merge_lists: ctypes.c_bool
    class internal_8:
        tqh_first: ctypes._Pointer[QemuOpts]
        tqh_last: ctypes._Pointer[ctypes._Pointer[QemuOpts]]

    head: internal_8
    desc: ctypes.Array[QemuOptDesc]

class QemuThread:
    thread: ctypes.c_ulong

class RAMBlock:
    rcu: rcu_head
    mr: ctypes._Pointer[MemoryRegion]
    host: ctypes._Pointer[ctypes.c_ubyte]
    offset: ctypes.c_ulong
    used_length: ctypes.c_ulong
    max_length: ctypes.c_ulong
    resized: Callable[[ctypes._Pointer[ctypes.c_char], ctypes.c_ulong, ctypes.c_void_p], None]
    flags: ctypes.c_uint
    idstr: ctypes.Array[ctypes.c_char]
    class internal_1:
        le_next: ctypes._Pointer[RAMBlock]
        le_prev: ctypes._Pointer[ctypes._Pointer[RAMBlock]]

    next: internal_1
    class internal_2:
        lh_first: ctypes._Pointer[RAMBlockNotifier]

    ramblock_notifiers: internal_2
    fd: ctypes.c_int
    page_size: ctypes.c_ulong

class RAMBlockNotifier:
    pass

class ReadLineState:
    cmd_buf: ctypes.Array[ctypes.c_char]
    cmd_buf_index: ctypes.c_int
    cmd_buf_size: ctypes.c_int
    last_cmd_buf: ctypes.Array[ctypes.c_char]
    last_cmd_buf_index: ctypes.c_int
    last_cmd_buf_size: ctypes.c_int
    esc_state: ctypes.c_int
    esc_param: ctypes.c_int
    history: ctypes.Array[ctypes._Pointer[ctypes.c_char]]
    hist_entry: ctypes.c_int
    completion_finder: Callable[[ctypes.c_void_p, ctypes._Pointer[ctypes.c_char]], None]
    completions: ctypes.Array[ctypes._Pointer[ctypes.c_char]]
    nb_completions: ctypes.c_int
    completion_index: ctypes.c_int
    readline_func: Callable[[ctypes.c_void_p, ctypes._Pointer[ctypes.c_char], ctypes.c_void_p], None]
    readline_opaque: ctypes.c_void_p
    read_password: ctypes.c_int
    prompt: ctypes.Array[ctypes.c_char]
    printf_func: Callable[[ctypes.c_void_p, ctypes._Pointer[ctypes.c_char]], None]
    flush_func: Callable[[ctypes.c_void_p], None]
    opaque: ctypes.c_void_p

class SegmentCache:
    selector: ctypes.c_uint
    base: ctypes.c_uint
    limit: ctypes.c_uint
    flags: ctypes.c_uint

class String:
    pass

class SymbolicBranchMeta:
    pc: ctypes.c_ulong

class TaskStruct:
    tasks: ListHead
    pid: ctypes.c_uint
    tgid: ctypes.c_uint
    group_leader: ctypes.c_uint
    thread_group: ctypes.c_uint
    real_parent: ctypes.c_uint
    parent: ctypes.c_uint
    mm: ctypes.c_uint
    stack: ctypes.c_uint
    real_cred: ctypes.c_uint
    cred: ctypes.c_uint
    comm: ctypes.Array[ctypes.c_ubyte]
    files: ctypes.c_uint
    start_time: ctypes.c_uint
    children: ListHead
    sibling: ListHead

class TranslationBlock:
    pc: ctypes.c_uint
    cs_base: ctypes.c_uint
    flags: ctypes.c_uint
    size: ctypes.c_ushort
    icount: ctypes.c_ushort
    cflags: ctypes.c_uint
    invalid: ctypes.c_ushort
    was_split: ctypes.c_ubyte
    tc_ptr: ctypes.c_void_p
    tc_search: ctypes._Pointer[ctypes.c_ubyte]
    orig_tb: ctypes._Pointer[TranslationBlock]
    page_next: ctypes.Array[ctypes._Pointer[TranslationBlock]]
    page_addr: ctypes.Array[ctypes.c_ulong]
    jmp_reset_offset: ctypes.Array[ctypes.c_ushort]
    jmp_insn_offset: ctypes.Array[ctypes.c_ushort]
    jmp_list_next: ctypes.Array[ctypes.c_ulong]
    jmp_list_first: ctypes.c_ulong
    llvm_tc_ptr: ctypes._Pointer[ctypes.c_ubyte]
    llvm_tc_end: ctypes._Pointer[ctypes.c_ubyte]
    llvm_tb_next: ctypes.Array[ctypes._Pointer[TranslationBlock]]
    llvm_asm_ptr: ctypes._Pointer[ctypes.c_ubyte]
    llvm_fn_name: ctypes.Array[ctypes.c_char]

class Vec_CosiModule:
    pass

class Vec_CosiProc:
    pass

class VmAreaStruct:
    vm_mm: ctypes.c_uint
    vm_start: ctypes.c_uint
    vm_end: ctypes.c_uint
    vm_next: ctypes.c_uint
    vm_file: ctypes.c_uint
    vm_flags: ctypes.c_uint

class _IO_FILE:
    pass

class _panda_cb_list:
    entry: panda_cb_with_context
    owner: ctypes.c_void_p
    next: ctypes._Pointer[_panda_cb_list]
    prev: ctypes._Pointer[_panda_cb_list]
    enabled: ctypes.c_bool
    context: ctypes.c_void_p

class addr_struct:
    typ: AddrType
    val: ctypes.c_ulong
    off: ctypes.c_ushort
    flag: AddrFlag

class auxv_values:
    argc: ctypes.c_int
    argv_ptr_ptr: ctypes.c_uint
    arg_ptr: ctypes.Array[ctypes.c_uint]
    argv: ctypes.Array[ctypes.Array[ctypes.c_char]]
    envc: ctypes.c_int
    env_ptr_ptr: ctypes.c_uint
    env_ptr: ctypes.Array[ctypes.c_uint]
    envp: ctypes.Array[ctypes.Array[ctypes.c_char]]
    execfn_ptr: ctypes.c_uint
    execfn: ctypes.Array[ctypes.c_char]
    phdr: ctypes.c_uint
    entry: ctypes.c_uint
    ehdr: ctypes.c_uint
    hwcap: ctypes.c_uint
    hwcap2: ctypes.c_uint
    pagesz: ctypes.c_uint
    clktck: ctypes.c_uint
    phent: ctypes.c_uint
    phnum: ctypes.c_uint
    base: ctypes.c_uint
    flags: ctypes.c_uint
    uid: ctypes.c_uint
    euid: ctypes.c_uint
    gid: ctypes.c_uint
    egid: ctypes.c_uint
    secure: ctypes.c_bool
    random: ctypes.c_uint
    platform: ctypes.c_uint
    program_header: ctypes.c_uint
    minsigstksz: ctypes.c_uint

class breakpoints_head:
    tqh_first: ctypes._Pointer[CPUBreakpoint]
    tqh_last: ctypes._Pointer[ctypes._Pointer[CPUBreakpoint]]

class coalesced_ranges:
    tqh_first: ctypes._Pointer[CoalescedMemoryRange]
    tqh_last: ctypes._Pointer[ctypes._Pointer[CoalescedMemoryRange]]

class cred_info:
    uid_offset: ctypes.c_int
    gid_offset: ctypes.c_int
    euid_offset: ctypes.c_int
    egid_offset: ctypes.c_int

class dynamic_symbol_hook:
    library_name: ctypes.Array[ctypes.c_char]
    symbol: ctypes.Array[ctypes.c_char]
    cb: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[hook]], ctypes.c_bool]

class float_status:
    float_detect_tininess: ctypes.c_byte
    float_rounding_mode: ctypes.c_byte
    float_exception_flags: ctypes.c_ubyte
    floatx80_rounding_precision: ctypes.c_byte
    flush_to_zero: ctypes.c_char
    flush_inputs_to_zero: ctypes.c_char
    default_nan_mode: ctypes.c_char
    snan_bit_is_one: ctypes.c_char

class fs_info:
    f_path_dentry_offset: ctypes.c_int
    f_dentry_offset: ctypes.c_int
    f_path_mnt_offset: ctypes.c_int
    f_vfsmnt_offset: ctypes.c_int
    f_pos_offset: ctypes.c_int
    fdt_offset: ctypes.c_int
    fdtab_offset: ctypes.c_int
    fd_offset: ctypes.c_int

class hax_state:
    pass

class hax_tunnel:
    pass

class hax_vcpu_state:
    fd: ctypes.c_ulong
    vcpu_id: ctypes.c_int
    tunnel: ctypes._Pointer[hax_tunnel]
    iobuf: ctypes._Pointer[ctypes.c_ubyte]

class hook:
    addr: ctypes.c_uint
    asid: ctypes.c_uint
    type: panda_cb_type
    cb: hooks_panda_cb
    km: kernel_mode
    enabled: ctypes.c_bool
    sym: symbol
    context: ctypes.c_void_p

class hook_symbol_resolve:
    name: ctypes.Array[ctypes.c_char]
    offset: ctypes.c_uint
    hook_offset: ctypes.c_bool
    section: ctypes.Array[ctypes.c_char]
    cb: Callable[[ctypes._Pointer[hook_symbol_resolve], symbol, ctypes.c_uint], None]
    enabled: ctypes.c_bool
    id: ctypes.c_int

class icount_decr_u16:
    low: ctypes.c_ushort
    high: ctypes.c_ushort

class kernelinfo:
    name: ctypes._Pointer[ctypes.c_char]
    version: version
    task: task_info
    cred: cred_info
    mm: mm_info
    vma: vma_info
    fs: fs_info
    qstr: qstr_info
    path: path_info

class kvm_run:
    pass

class memory_access_desc:
    pc: ctypes.c_uint
    addr: ctypes.c_uint
    size: ctypes.c_ulong
    buf: ctypes._Pointer[ctypes.c_ubyte]
    on_before: ctypes.c_bool
    on_after: ctypes.c_bool
    on_read: ctypes.c_bool
    on_write: ctypes.c_bool
    on_virtual: ctypes.c_bool
    on_physical: ctypes.c_bool
    hook: ctypes._Pointer[memory_hooks_region]

class memory_hooks_region:
    start_address: ctypes.c_uint
    stop_address: ctypes.c_uint
    enabled: ctypes.c_bool
    on_before: ctypes.c_bool
    on_after: ctypes.c_bool
    on_read: ctypes.c_bool
    on_write: ctypes.c_bool
    on_virtual: ctypes.c_bool
    on_physical: ctypes.c_bool
    cb: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[memory_access_desc]], None]

class memory_listeners_as:
    tqh_first: ctypes._Pointer[MemoryListener]
    tqh_last: ctypes._Pointer[ctypes._Pointer[MemoryListener]]

class mm_info:
    size: ctypes.c_ulong
    mmap_offset: ctypes.c_int
    pgd_offset: ctypes.c_int
    arg_start_offset: ctypes.c_int
    start_brk_offset: ctypes.c_int
    brk_offset: ctypes.c_int
    start_stack_offset: ctypes.c_int

class mon_fd_t:
    pass

class osi_module_struct:
    modd: ctypes.c_uint
    base: ctypes.c_uint
    size: ctypes.c_uint
    file: ctypes._Pointer[ctypes.c_char]
    name: ctypes._Pointer[ctypes.c_char]
    offset: ctypes.c_uint
    flags: ctypes.c_uint

class osi_page_struct:
    start: ctypes.c_uint
    len: ctypes.c_uint

class osi_proc_handle_struct:
    taskd: ctypes.c_uint
    asid: ctypes.c_uint

class osi_proc_mem:
    start_brk: ctypes.c_uint
    brk: ctypes.c_uint

class osi_proc_struct:
    taskd: ctypes.c_uint
    pgd: ctypes.c_uint
    asid: ctypes.c_uint
    pid: ctypes.c_int
    ppid: ctypes.c_int
    name: ctypes._Pointer[ctypes.c_char]
    pages: ctypes._Pointer[osi_page_struct]
    create_time: ctypes.c_ulong

class osi_thread_struct:
    pid: ctypes.c_int
    tid: ctypes.c_int

class panda_arg:
    argptr: ctypes._Pointer[ctypes.c_char]
    key: ctypes._Pointer[ctypes.c_char]
    value: ctypes._Pointer[ctypes.c_char]

class panda_arg_list:
    nargs: ctypes.c_int
    list: ctypes._Pointer[panda_arg]
    plugin_name: ctypes._Pointer[ctypes.c_char]

class panda_plugin:
    name: ctypes._Pointer[ctypes.c_char]
    plugin: ctypes.c_void_p
    unload: ctypes.c_bool
    exported_symbols: ctypes.c_bool

class path_info:
    d_name_offset: ctypes.c_int
    d_iname_offset: ctypes.c_int
    d_parent_offset: ctypes.c_int
    d_op_offset: ctypes.c_int
    d_dname_offset: ctypes.c_int
    mnt_root_offset: ctypes.c_int
    mnt_parent_offset: ctypes.c_int
    mnt_mountpoint_offset: ctypes.c_int

class qemu_work_item:
    next: ctypes._Pointer[qemu_work_item]
    func: ctypes.c_void_p
    data: ctypes.c_ulong
    free: ctypes.c_bool
    exclusive: ctypes.c_bool
    done: ctypes.c_bool

class qstr_info:
    size: ctypes.c_ulong
    name_offset: ctypes.c_ulong

class query_result:
    num_labels: ctypes.c_uint
    ls: ctypes.c_void_p
    it_end: ctypes.c_void_p
    it_curr: ctypes.c_void_p
    tcn: ctypes.c_uint
    cb_mask: ctypes.c_ubyte

class rcu_head:
    next: ctypes._Pointer[rcu_head]
    func: Callable[[ctypes._Pointer[rcu_head]], None]

class subregions:
    tqh_first: ctypes._Pointer[MemoryRegion]
    tqh_last: ctypes._Pointer[ctypes._Pointer[MemoryRegion]]

class symbol:
    address: ctypes.c_uint
    value: ctypes.c_uint
    symtab_idx: ctypes.c_int
    reloc_type: ctypes.c_int
    name: ctypes.Array[ctypes.c_char]
    section: ctypes.Array[ctypes.c_char]

class symbol_hook:
    name: ctypes.Array[ctypes.c_char]
    offset: ctypes.c_uint
    hook_offset: ctypes.c_bool
    section: ctypes.Array[ctypes.c_char]
    type: panda_cb_type
    cb: hooks_panda_cb

class syscall_ctx:
    no: ctypes.c_int
    asid: ctypes.c_uint
    retaddr: ctypes.c_uint
    args: ctypes.Array[ctypes.Array[ctypes.c_ubyte]]

class task_info:
    per_cpu_offsets_addr: ctypes.c_ulong
    per_cpu_offset_0_addr: ctypes.c_ulong
    switch_task_hook_addr: ctypes.c_ulong
    current_task_addr: ctypes.c_ulong
    init_addr: ctypes.c_ulong
    size: ctypes.c_ulong
    tasks_offset: ctypes.c_int
    next_task_offset: ctypes.c_int
    pid_offset: ctypes.c_int
    tgid_offset: ctypes.c_int
    group_leader_offset: ctypes.c_int
    thread_group_offset: ctypes.c_int
    real_parent_offset: ctypes.c_int
    p_opptr_offset: ctypes.c_int
    parent_offset: ctypes.c_int
    p_pptr_offset: ctypes.c_int
    mm_offset: ctypes.c_int
    stack_offset: ctypes.c_int
    real_cred_offset: ctypes.c_int
    cred_offset: ctypes.c_int
    comm_offset: ctypes.c_int
    comm_size: ctypes.c_ulong
    files_offset: ctypes.c_int
    start_time_offset: ctypes.c_int

class version:
    a: ctypes.c_int
    b: ctypes.c_int
    c: ctypes.c_int

class vma_info:
    size: ctypes.c_ulong
    vm_mm_offset: ctypes.c_int
    vm_start_offset: ctypes.c_int
    vm_end_offset: ctypes.c_int
    vm_next_offset: ctypes.c_int
    vm_file_offset: ctypes.c_int
    vm_flags_offset: ctypes.c_int

class watchpoints_head:
    tqh_first: ctypes._Pointer[CPUWatchpoint]
    tqh_last: ctypes._Pointer[ctypes._Pointer[CPUWatchpoint]]

class hooks_panda_cb:
    before_tcg_codegen: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[hook]], None]
    before_block_translate: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes._Pointer[hook]], None]
    after_block_translate: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[hook]], None]
    before_block_exec_invalidate_opt: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[hook]], ctypes.c_bool]
    before_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[hook]], None]
    after_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes.c_ubyte, ctypes._Pointer[hook]], None]
    start_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[hook]], None]
    end_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes._Pointer[hook]], None]

class panda_cb:
    before_block_exec_invalidate_opt: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], ctypes.c_bool]
    before_tcg_codegen: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    before_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    after_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes.c_ubyte], None]
    before_block_translate: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], None]
    after_block_translate: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    after_cpu_exec_enter: Callable[[ctypes._Pointer[CPUState]], None]
    before_cpu_exec_exit: Callable[[ctypes._Pointer[CPUState], ctypes.c_bool], None]
    insn_translate: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_bool]
    insn_exec: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_int]
    after_insn_translate: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_bool]
    after_insn_exec: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_int]
    virt_mem_before_read: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
    virt_mem_before_write: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    phys_mem_before_read: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
    phys_mem_before_write: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    virt_mem_after_read: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    virt_mem_after_write: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    phys_mem_after_read: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    phys_mem_after_write: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    mmio_after_read: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ulong]], None]
    mmio_before_write: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ulong]], None]
    hd_read: Callable[[ctypes._Pointer[CPUState]], None]
    hd_write: Callable[[ctypes._Pointer[CPUState]], None]
    guest_hypercall: Callable[[ctypes._Pointer[CPUState]], ctypes.c_bool]
    monitor: Callable[[ctypes._Pointer[Monitor], ctypes._Pointer[ctypes.c_char]], ctypes.c_int]
    qmp: Callable[[ctypes._Pointer[ctypes.c_char], ctypes._Pointer[ctypes.c_char], ctypes._Pointer[ctypes._Pointer[ctypes.c_char]]], ctypes.c_bool]
    cpu_restore_state: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    before_loadvm: Callable[[], ctypes.c_int]
    asid_changed: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], ctypes.c_bool]
    replay_hd_transfer: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
    replay_before_dma: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_ubyte], ctypes.c_ulong, ctypes.c_ulong, ctypes.c_bool], None]
    replay_after_dma: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_ubyte], ctypes.c_ulong, ctypes.c_ulong, ctypes.c_bool], None]
    replay_handle_packet: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_ubyte], ctypes.c_ulong, ctypes.c_ubyte, ctypes.c_ulong], None]
    replay_net_transfer: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong], None]
    replay_serial_receive: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ubyte], None]
    replay_serial_read: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ubyte], None]
    replay_serial_send: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ubyte], None]
    replay_serial_write: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ubyte], None]
    after_machine_init: Callable[[ctypes._Pointer[CPUState]], None]
    after_loadvm: Callable[[ctypes._Pointer[CPUState]], None]
    top_loop: Callable[[ctypes._Pointer[CPUState]], None]
    during_machine_init: Callable[[ctypes._Pointer[MachineState]], None]
    main_loop_wait: Callable[[], None]
    pre_shutdown: Callable[[], None]
    unassigned_io_read: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ulong, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ulong]], ctypes.c_bool]
    unassigned_io_write: Callable[[ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong], ctypes.c_bool]
    before_handle_exception: Callable[[ctypes._Pointer[CPUState], ctypes.c_int], ctypes.c_int]
    before_handle_interrupt: Callable[[ctypes._Pointer[CPUState], ctypes.c_int], ctypes.c_int]
    start_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    end_block_exec: Callable[[ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    cbaddr: Callable[[], None]

class panda_cb_with_context:
    before_block_exec_invalidate_opt: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], ctypes.c_bool]
    before_tcg_codegen: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    before_block_exec: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    after_block_exec: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock], ctypes.c_ubyte], None]
    before_block_translate: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint], None]
    after_block_translate: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    after_cpu_exec_enter: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState]], None]
    before_cpu_exec_exit: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_bool], None]
    insn_translate: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_bool]
    insn_exec: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_int]
    after_insn_translate: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_bool]
    after_insn_exec: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint], ctypes.c_int]
    virt_mem_before_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
    virt_mem_before_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    phys_mem_before_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
    phys_mem_before_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    virt_mem_after_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    virt_mem_after_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    phys_mem_after_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    phys_mem_after_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ubyte]], None]
    mmio_after_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ulong]], None]
    mmio_before_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ulong]], None]
    hd_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState]], None]
    hd_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState]], None]
    guest_hypercall: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState]], ctypes.c_bool]
    monitor: Callable[[ctypes.c_void_p, ctypes._Pointer[Monitor], ctypes._Pointer[ctypes.c_char]], ctypes.c_int]
    qmp: Callable[[ctypes.c_void_p, ctypes._Pointer[ctypes.c_char], ctypes._Pointer[ctypes.c_char], ctypes._Pointer[ctypes._Pointer[ctypes.c_char]]], ctypes.c_bool]
    cpu_restore_state: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    before_loadvm: Callable[[ctypes.c_void_p], ctypes.c_int]
    asid_changed: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint], ctypes.c_bool]
    replay_hd_transfer: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_ulong], None]
    replay_before_dma: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_ubyte], ctypes.c_ulong, ctypes.c_ulong, ctypes.c_bool], None]
    replay_after_dma: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_ubyte], ctypes.c_ulong, ctypes.c_ulong, ctypes.c_bool], None]
    replay_handle_packet: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[ctypes.c_ubyte], ctypes.c_ulong, ctypes.c_ubyte, ctypes.c_ulong], None]
    replay_net_transfer: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong], None]
    replay_serial_receive: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ubyte], None]
    replay_serial_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ubyte], None]
    replay_serial_send: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ubyte], None]
    replay_serial_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_uint, ctypes.c_ubyte], None]
    after_machine_init: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState]], None]
    after_loadvm: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState]], None]
    top_loop: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState]], None]
    during_machine_init: Callable[[ctypes.c_void_p, ctypes._Pointer[MachineState]], None]
    main_loop_wait: Callable[[ctypes.c_void_p], None]
    pre_shutdown: Callable[[ctypes.c_void_p], None]
    unassigned_io_read: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ulong, ctypes.c_ulong, ctypes._Pointer[ctypes.c_ulong]], ctypes.c_bool]
    unassigned_io_write: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_uint, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong], ctypes.c_bool]
    before_handle_exception: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_int], ctypes.c_int]
    before_handle_interrupt: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes.c_int], ctypes.c_int]
    start_block_exec: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    end_block_exec: Callable[[ctypes.c_void_p, ctypes._Pointer[CPUState], ctypes._Pointer[TranslationBlock]], None]
    cbaddr: Callable[[], None]

class device_endian(IntEnum):
    DEVICE_LITTLE_ENDIAN: int = 2
    DEVICE_BIG_ENDIAN: int = 1
    DEVICE_NATIVE_ENDIAN: int = 0

class QemuOptType(IntEnum):
    QEMU_OPT_SIZE: int = 3
    QEMU_OPT_NUMBER: int = 2
    QEMU_OPT_BOOL: int = 1
    QEMU_OPT_STRING: int = 0

class kernel_mode(IntEnum):
    MODE_USER_ONLY: int = 2
    MODE_KERNEL_ONLY: int = 1
    MODE_ANY: int = 0

