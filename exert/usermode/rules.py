from exert.usermode.context import Context

class Rule:
    _cache = {}

    def __init__(self):
        self.key = None

    def test(self, context, address, clear_cache = False):
        return self.test_all(context, {address}, clear_cache)

    def test_all(self, context, addresses, clear_cache = False):
        assert isinstance(context, Context)
        assert isinstance(addresses, set)

        if len(addresses) == 0:
            return addresses

        # For efficiency, we memoize the test() method by caching results
        if clear_cache:
            Rule._cache.clear()

        results = set()
        for address in addresses:
            key = f'{address}:{str(self)}'
            if key not in Rule._cache:
                # We may end up testing ourselves, so temporarily store something
                # to pass the above check
                Rule._cache[key] = set()
                Rule._cache[key] = self._test(context, address)
            results |= Rule._cache[key]

        return results

    def _test(self, context, address):
        return {address}

    def _get_key(self):
        return 'Rule'

    def __str__(self):
        if not self.key:
            self.key = self._get_key()
        return self.key

class Any(Rule):
    def __init__(self, *rules):
        super().__init__()
        self.rules = rules

    def _get_key(self):
        return f"Any({', '.join(str(r) for r in self.rules)})"

    def _test(self, context, address):
        #TODO
        return {address}

class Int(Rule):
    def __init__(self, size = 4, signed = True, min_value = None, max_value = None):
        super().__init__()
        self.size = size
        self.signed = signed
        self.min_value = min_value
        self.max_value = max_value if max_value is not None else min_value

    def _get_key(self):
        return f'Int({self.size}, {self.signed}, {self.min_value}, {self.max_value})'

    def _test(self, context, address):
        size = context.word_size if self.size is None else self.size
        val, address = context.next_int(address, size, self.signed)
        if val is None:
            return set()
        if self.min_value is not None and val < self.min_value:
            return set()
        if self.max_value is not None and val > self.max_value:
            return set()
        return {address}

class Bool(Int):
    def __init__(self):
        super().__init__(size = 1, min_value = 0, max_value = 1)

    def _get_key(self):
        return 'Bool'

class Pointer(Rule):
    def __init__(self, rule = None):
        super().__init__()
        self.rule = rule

    def _get_key(self):
        return f'Pointer({str(self.rule)})'

    def _test(self, context, address):
        pointer, address = context.next_pointer(address)
        if pointer is None or (self.rule and not self.rule.test(context, pointer)):
            return set()
        return {address}
    
class Union(Rule):
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules
        super().__init__()

    def _test(self, context, address):
        results = set()

        for rule in self.rules:
            results = results | rule.test(context, address)

        return results
    
    def _get_key(self):
        rule_string = '['

        for rule in self.rules:
            rule_string = rule_string + str(rule) + ', '

        rule_string = rule_string + ']'

        return f'Union({self.name}, [{rule_string}])'

class Array(Rule):
    def __init__(self, rule, count_min, count_max):
        super().__init__()
        self.rule = rule
        self.count_min = count_min
        self.count_max = count_max

    def _get_key(self):
        return f'Array({str(self.rule)}, {self.count_min}, {self.count_max})'

    def _test(self, context, address):
        passing = {address}
        for _ in range(0, self.count_min):
            passing = self.rule.test_all(context, passing)
        to_test = passing
        for _ in range(self.count_min, self.count_max):
            elem_passing = self.rule.test_all(context, to_test)
            to_test = elem_passing - passing
            passing |= elem_passing
        return passing

class Field(Rule):
    def __init__(self, name, rule):
        super().__init__()
        self.name = name
        self.rule = rule

    def _get_key(self):
        return f"Field('{self.name}', {str(self.rule)})"

    def _test(self, context, address):
        return self.rule.test(context, address)

class FieldGroup:
    def __init__(self, fields, condition=None):
        self.fields = fields
        for field in self.fields:
            assert isinstance(field, Field)
        self.condition = condition
        self.fields_addresses = None

    def test_all(self, context, addresses):
        self.fields_addresses = dict()
        passing = set()
        for field in self.fields:
            field_addresses = field.test_all(context, addresses)
            self.fields_addresses.update({field._get_key(): field_addresses})
            passing |= field_addresses
        return passing

    def __str__(self):
        fields_str = ', '.join(str(f) for f in self.fields)
        cond_str = 'None' if self.condition is None else f"'{self.condition}'"
        return f'FieldGroup([{fields_str}], {cond_str})'
    
    def get_field_addresses(self, context, address):
        if (self.fields_addresses):
            return self.fields_addresses
        else:
            self.test_all(context, {address})
            return self.fields_addresses

class Struct(Rule):
    def __init__(self, name, field_groups):
        super().__init__()
        self.name = name
        self.field_groups = field_groups
        self.fields_addresses = None

    def _get_key(self):
        groups_str = ', '.join([str(g) for g in self.field_groups])
        return f"Struct('{self.name}', [{groups_str}])"

    def _test(self, context, address):
        passing = {address}
        self.fields_addresses = dict()
        for group in self.field_groups:
            if group.condition:
                passing |= group.test_all(context, passing)
                self.fields_addresses.update(group.get_field_addresses(context, address))
            else:
                passing = group.test_all(context, passing)
                self.fields_addresses.update(group.get_field_addresses(context, address))
        return passing
    
    def get_field_addresses(self, context, address):
        if (self.fields_addresses):
            return self.fields_addresses
        else:
            self._test(context, address)
            return self.fields_addresses

class _Struct(Struct):
    def _get_key(self):
        return f'{self.__class__.__name__}'
    
class _Union(Union):
    def _get_key(self):
        return f'{self.__class__.__name__}'

class _Atomic(_Struct):
    def __init__(self):
        super().__init__('atomic_t', [FieldGroup([
            Field('counter', Int())
        ])])
ATOMIC = _Atomic()

class _LoadWeight(_Struct):
    def __init__(self):
        super().__init__('load_weight', [FieldGroup([
            Field('weight', Int(size = None, signed = False)),
            Field('inv_weight', Int(signed = False))
        ])])
LOAD_WEIGHT = _LoadWeight()

class _RBNode(_Struct):
    def __init__(self):
        super().__init__('rb_node', [FieldGroup([
            Field('__rb_parent_color', Int(size = None, signed = False)),
            Field('rb_right', Pointer(self)),
            Field('rb_left', Pointer(self))
        ])])
RB_NODE = _RBNode()

class _LListNode(_Struct):
    def __init__(self):
        super().__init__('llist_node', [FieldGroup([
            Field('next', Pointer(self))
        ])])
LLIST_NODE = _LListNode()

class _SchedAvg(_Struct):
    def __init__(self):
        super().__init__('sched_avg', [FieldGroup([
            Field('last_update_time', Int(size = 8, signed = False)),
            Field('load_sum', Int(size = 8, signed = False)),
            Field('util_sum', Int(signed = False)),
            Field('period_contrib', Int(signed = False)),
            Field('load_avg', Int(size = None, signed = False)),
            Field('util_avg', Int(size = None, signed = False))
        ])])
SCHED_AVG = _SchedAvg()

class _ListHead(_Struct):
    def __init__(self):
        super().__init__('list_head', [FieldGroup([
            Field('next', Pointer(self)),
            Field('prev', Pointer(self))
        ])])

    def _test(self, context, address):
        original = address
        next_pointer, address = context.next_pointer(address)
        if next_pointer is None:
            return set()
        next_prev_address = next_pointer + context.word_size
        next_prev_pointer = context.read_pointer(next_prev_address)
        if next_prev_pointer != original:
            return set()

        prev_pointer, address = context.next_pointer(address)
        if prev_pointer is None:
            return set()
        prev_next_address = prev_pointer + 0
        prev_next_pointer = context.read_pointer(prev_next_address)
        if prev_next_pointer != original:
            return set()

        return {address}
LIST_HEAD = _ListHead()

class _SchedInfo(_Struct):
    def __init__(self):
        super().__init__('sched_info', [FieldGroup([
                Field('pcount', Int(size = None, signed = False)),
                Field('run_delay', Int(size = 8, signed = False)),
                Field('last_arrival', Int(size = 8, signed = False)),
                Field('last_queued', Int(size = 8, signed = False))
        ])])
SCHED_INFO = _SchedInfo()

class _SchedStatistics(_Struct):
    def __init__(self):
        super().__init__('sched_statistics', [FieldGroup([
            Field('wait_start', Int(size = 8, signed = False)),
            Field('wait_max', Int(size = 8, signed = False)),
            Field('wait_count', Int(size = 8, signed = False)),
            Field('wait_sum', Int(size = 8, signed = False)),
            Field('iowait_count', Int(size = 8, signed = False)),
            Field('iowait_sum', Int(size = 8, signed = False)),
            Field('sleep_start', Int(size = 8, signed = False)),
            Field('sleep_max', Int(size = 8, signed = False)),
            Field('sum_sleep_runtime', Int(size = 8)),
            Field('block_start', Int(size = 8, signed = False)),
            Field('block_max', Int(size = 8, signed = False)),
            Field('exec_max', Int(size = 8, signed = False)),
            Field('slice_max', Int(size = 8, signed = False)),
            Field('nr_migrations_cold', Int(size = 8, signed = False)),
            Field('nr_failed_migrations_affine', Int(size = 8, signed = False)),
            Field('nr_failed_migrations_running', Int(size = 8, signed = False)),
            Field('nr_failed_migrations_hot', Int(size = 8, signed = False)),
            Field('nr_forced_migrations', Int(size = 8, signed = False)),
            Field('nr_wakeups', Int(size = 8, signed = False)),
            Field('nr_wakeups_sync', Int(size = 8, signed = False)),
            Field('nr_wakeups_migrate', Int(size = 8, signed = False)),
            Field('nr_wakeups_local', Int(size = 8, signed = False)),
            Field('nr_wakeups_remote', Int(size = 8, signed = False)),
            Field('nr_wakeups_affine', Int(size = 8, signed = False)),
            Field('nr_wakeups_affine_attempts', Int(size = 8, signed = False)),
            Field('nr_wakeups_passive', Int(size = 8, signed = False)),
            Field('nr_wakeups_idle', Int(size = 8, signed = False))
        ])])
SCHED_STATISTICS = _SchedStatistics()

class _KTimeT(_Struct): #supposed to be a union
    def __init__(self):
        super().__init__('timerqueue_node', [
            FieldGroup([
                Field('tv64', Int(size = 8))
            ])
        ])
KTIME_T = _KTimeT()

class _HListNode(_Struct): #supposed to be a union
    def __init__(self):
        super().__init__('hlist_node', [
            FieldGroup([
	        Field('next', Pointer(self)),
	        Field('pprev', Pointer(Pointer(self)))
            ])
        ])
HLIST_NODE = _HListNode()

class _HListHead(_Struct): #supposed to be a union
    def __init__(self):
        super().__init__('hlist_head', [
            FieldGroup([
	        Field('first', Pointer(HLIST_NODE)) #struct hlist_node *first;
            ])
        ])
HLIST_HEAD = _HListHead()

class _TimerQueueNode(_Struct):
    def __init__(self):
        super().__init__('timerqueue_node', [FieldGroup([
            Field('node', RB_NODE),
            Field('expires', KTIME_T)
        ])])
TIMERQUEUENODE = _TimerQueueNode()

class _LockdepSubclassKey(_Struct):
    def __init__(self):
        super().__init__('lockdep_subclass_key', [FieldGroup([
            Field('__one_byte', Int(size = 1))
        ])])
LOCKDEP_SUBCLASS_KEY = _LockdepSubclassKey() #TODO  __attribute__ ((__packed__));

class _LockClassKey(_Struct):
    def __init__(self):
        super().__init__('lock_class_key', [FieldGroup([
            Field('subkeys', Array(LOCKDEP_SUBCLASS_KEY, 8, 8))
        ])])
LOCK_CLASS_KEY = _LockClassKey()

class _StackTrace(_Struct):
    def __init__(self):
        super().__init__('stack_trace', [
            FieldGroup([
                Field('nr_entries', Int(signed = False)),
                Field('max_entries', Int(signed = False)),
                Field('entries', Pointer(Int(size = None, signed = False))),
                Field('skip', Int())
            ])
        ])
STACK_TRACE = _StackTrace()

class _LockClass(_Struct):
    def __init__(self):
        super().__init__('lock_class', [
            FieldGroup([
                Field('hash_entry', LIST_HEAD),
                Field('lock_entry', LIST_HEAD),
                Field('key', Pointer(LOCKDEP_SUBCLASS_KEY)),
                Field('subclass', Int(signed = False)),
                Field('dep_gen_id', Int(signed = False)),
                Field('usage_mask', Int(size = None, signed = False)),
                Field('usage_traces', Array(STACK_TRACE, 13,13)),
                Field('locks_after', LIST_HEAD),
                Field('locks_before', LIST_HEAD),
                Field('version', Int(signed = False)),
                Field('ops', Int(size = None, signed = False)),
                Field('name', Pointer(Int(size = 1))),
                Field('name_version', Int())
            ]),
            FieldGroup([
                Field('hash_entry', LIST_HEAD),
                Field('contention_point', Array(Int(size = None, signed = False), 4, 4)),
                Field('contending_point', Array(Int(size = None, signed = False), 4, 4))
            ], 'CONFIG_LOCK_STAT')
        ])
LOCK_CLASS = _LockClass()

class _LockdepMap(_Struct):
    def __init__(self):
        super().__init__('lockdep_map', [
            FieldGroup([
                Field('key', Pointer(LOCK_CLASS_KEY)),
                Field('class_cache', Array(Pointer(LOCK_CLASS), 2, 2)),
                Field('name', Pointer(Int(size = 1)))
            ]),
        FieldGroup([
            Field('cpu', Int()),
            Field('ip', Int(size = None, signed = False))
            ],'CONFIG_LOCK_STAT')
])
LOCKDEP_MAP = _LockdepMap()

class _ArchSpinlockT(_Struct):
    def __init__(self):
        super().__init__('arch_spinlock_t', [
             FieldGroup([
                Field('slock', Int(signed = False))
            ])#please look at the documentation for arch_spinlock_t
])
ARCH_SPINLOCK_T = _ArchSpinlockT()

class _RawSpinlockT(_Struct):
    def __init__(self):
        super().__init__('raw_spinlock_t', [
            FieldGroup([
                Field('raw_lock', ARCH_SPINLOCK_T)
            ]),
            FieldGroup([
                Field('break_lock', Int(signed = False))
            ], 'CONFIG_GENERIC_LOCKBREAK'),
            FieldGroup([
                Field('magic', Int(signed = False)),
                Field('owner_cpu', Int(signed = False)),
                Field('owner', Pointer())
            ], 'CONFIG_DEBUG_SPINLOCK'),
            FieldGroup([
                Field('dep_map', LOCKDEP_MAP)
            ], 'CONFIG_DEBUG_SPINLOCK')
        ]) #raw_spinlock_t, not spinlock
RAW_SPINLOCK_T = _RawSpinlockT()

class _SeqCountT(_Struct):
    def __init__(self):
        super().__init__('seqcount_t', [
            FieldGroup([
                Field('sequence', Int(signed = False))
            ]),
            FieldGroup([
                Field('dep_map', LOCKDEP_MAP)
            ], 'CONFIG_DEBUG_LOCK_ALLOC')
        ])
SEQCOUNT_T = _SeqCountT() # seqcount_t

class _HRTimerClockBase(_Struct):
    def __init__(self):
        super().__init__('hrtimer_clock_base', [
            FieldGroup([
                # Field('cpu_base', Pointer(HRTIMER_CPU_BASE)),
                Field('cpu_base', Pointer()),
                Field('index', Int()),
                Field('clockid', Int()), #clockid_t
                Field('get_time', Pointer()), #ktime_t			(*get_time)(void);
                Field('offset', KTIME_T)
            ])
        ])
#TODO this is an  __attribute__((__aligned__(HRTIMER_CLOCK_BASE_ALIGN)));
HRTIMER_CLOCK_BASE = _HRTimerClockBase()

class _HRTimer(_Struct):
    def __init__(self):
        super().__init__('hrtimer', [
            FieldGroup([
                Field('node', TIMERQUEUENODE),
                Field('_softexpires', KTIME_T),
                Field('function', Pointer()), # enum hrtimer_restart		(*function)(struct hrtimer *);
                Field('base', Pointer(HRTIMER_CLOCK_BASE)),
                Field('state', Int(size = 1, signed = False)),
                Field('is_rel', Int(size = 1, signed = False))
            ]),
            FieldGroup([
                Field('start_pid', Int()),
                Field('start_site', Pointer()),
                Field('start_comm', Array(Int(size = 1), 16, 16))
            ], 'CONFIG_TIMER_STATS')
        ])
HRTIMER = _HRTimer()

class _HrTimerCpuBase(_Struct):
    def __init__(self):
        super().__init__('hrtimer_cpu_base', [
            FieldGroup([
                Field('lock', RAW_SPINLOCK_T),
                Field('seq', SEQCOUNT_T),
                Field('running', Pointer(HRTIMER)),
	            Field('cpu', Int(signed = False)),
	            Field('active_bases', Int(signed = False)),
	            Field('clock_was_set_seq', Int(signed = False)),
	            Field('migration_enabled', Bool()),
	            Field('nohz_active', Bool())
            ]),
            FieldGroup([
                #in_hrtirq : 1, hres_active : 1,hang_detected : 1
                Field('bit_field', Int(signed = False)),
                Field('expires_next', KTIME_T),
                Field('next_timer', Pointer(HRTIMER)),
	            Field('nr_events', Int(signed = False)),
	            Field('nr_retries', Int(signed = False)),
	            Field('nr_hangs', Int(signed = False)),
	            Field('max_hang_time', Int(signed = False))
            ], 'CONFIG_HIGH_RES_TIMERS'),
            FieldGroup([
                #clock_base[HRTIMER_MAX_CLOCK_BASES];
                Field('clock_base', Array(HRTIMER_CLOCK_BASE, 4, 4))
            ])
        ])
HRTIMER_CPU_BASE = _HrTimerCpuBase() #TODO this is an  ____cacheline_aligned;

class _SchedEntity(_Struct):
    def __init__(self):
        super().__init__('sched_entity', [
            FieldGroup([
                Field('load', LOAD_WEIGHT),
                Field('run_node', RB_NODE),
                Field('group_node', LIST_HEAD),
                Field('on_rq', Int(signed = False)),
                Field('exec_start', Int(size = 8, signed = False)),
                Field('sum_exec_runtime', Int(size = 8, signed = False)),
                Field('vruntime', Int(size = 8, signed = False)),
                Field('prev_sum_exec_runtime', Int(size = 8, signed = False)),
                Field('nr_migrations', Int(size = 8, signed = False))
            ]),
            FieldGroup([
                Field('statistics', SCHED_STATISTICS)
            ], 'CONFIG_SCHEDSTATS'),
            FieldGroup([
                Field('depth', Int()),
                Field('parent', Pointer(self)),
                Field('cfs_rq', Pointer()), #struct cfs_rq*
                Field('my_q', Pointer()) #struct cfs_rq*
            ], 'CONFIG_FAIR_GROUP_SCHED'),
            FieldGroup([
	            Field('avg', SCHED_AVG)
            ], 'CONFIG_SMP')
        ])
SCHED_ENTITY = _SchedEntity()

class _SchedRTEntity(_Struct):
    def __init__(self):
        super().__init__('sched_rt_entity', [
            FieldGroup([
                Field('run_list', LIST_HEAD),
                Field('timeout', Int(size = None, signed = False)),
                Field('watchdog_stamp', Int(size = None, signed = False)),
                Field('time_slice', Int(signed = False)),
                Field('back', Pointer(self))
            ]),
            FieldGroup([
                Field('parent', Pointer(self)),
                Field('rt_rq', Pointer()), #struct rt_rq*
                Field('my_q', Pointer())  #struct rt_rq*
            ], 'CONFIG_RT_GROUP_SCHED')
        ])
SCHED_RT_ENTITY = _SchedRTEntity()

class _SchedDLEntity(_Struct):
    def __init__(self):
        super().__init__('sched_dl_entity', [
            FieldGroup([
            	Field('rb_node', RB_NODE),
                Field('dl_runtime', Int(size = 8, signed = False)),
                Field('dl_deadline', Int(size = 8, signed = False)),
                Field('dl_period', Int(size = 8, signed = False)),
                Field('dl_bw', Int(size = 8, signed = False)),
                Field('runtime', Int(size = 8)),
                Field('deadline', Int(size = 8, signed = False)),
                Field('flags', Int(signed = False)),
                Field('dl_throttled', Int()),
                Field('dl_new', Int()),
                Field('dl_boosted', Int()),
                Field('dl_yielded', Int()),
                Field('dl_timer', HRTIMER)
            ])
        ])
SCHED_DL_ENTITY = _SchedDLEntity()

class _CpuMask(_Struct):
    def __init__(self):
        super().__init__('cpumask_t', [FieldGroup([
            # Might still be good as a user parameter.
            # Even still, 8192 is the max
            Field('bits', Array(Int(size = None, signed = False), 1, 8192))
        ])])
CPUMASK = _CpuMask()

class _LoadWeight(_Struct):
    def __init__(self):
        super().__init__('load_weight', [FieldGroup([
            Field('weight', Int(size = None, signed = False)),
            Field('inv_weight', Int(size = 4, signed = False))
        ])])
LOAD_WEIGHT = _LoadWeight()

class _RBRoot(_Struct):
    def __init__(self):
        super().__init__('rb_root', [FieldGroup([
            Field('rb_node', Pointer(RB_NODE))
        ])])
RB_ROOT = _RBRoot()

class _CFSRQ(_Struct):
    def __init__(self):
        super().__init__('cfs_rq', [
            FieldGroup([
                Field('load', LOAD_WEIGHT),
                Field('nr_running', Int(signed = False)),
                Field('h_nr_running', Int(signed = False)),
                Field('exec_clock', Int(size = 8, signed = False)),
                Field('min_vruntime', Int(size = 8, signed = False))
            ]),
            FieldGroup([
                Field('min_vruntime_copy', Int(size = 8, signed = False))
            ], '!CONFIG_64BIT'),
            FieldGroup([
                Field('tasks_timeline', RB_ROOT),
                Field('rb_leftmost', Pointer(RB_NODE))
            ]),
            FieldGroup([
                Field('curr', Pointer(SCHED_ENTITY)),
                Field('next', Pointer(SCHED_ENTITY)),
                Field('last', Pointer(SCHED_ENTITY)),
                Field('skip', Pointer(SCHED_ENTITY))
            ]),
            FieldGroup([
                Field('nr_spread_over', Int(signed = False))
            ], 'CONFIG_SCHED_DEBUG'),
            FieldGroup([
                Field('avg', _SchedAvg()),
                Field('runnable_load_sum', Int(size = 8, signed = False)),
                Field('runnable_load_sum', Int(size = None, signed = False))
            ], 'CONFIG_SMP'),
            FieldGroup([
                Field('tg_load_avg_contrib', Int(size = None, signed = False))
            ], 'CONFIG_FAIR_GROUP_SCHED'),
            FieldGroup([
                Field('removed_load_avg', Int(size = None, signed = False)),
                # atomic_long_t removed_load_avg, removed_util_avg;
                Field('removed_util_avg', Int(size = 8, signed = False))
            ]),
            FieldGroup([
                Field('load_last_update_time_copy', Int(size = 8, signed = False))
            ], 'CONFIG_64BIT'),
            FieldGroup([
                Field('h_load', Int(size = None, signed = False)),
                Field('last_h_load_update', Int(size = 8, signed = False)),
                Field('h_load_next', Pointer(SCHED_ENTITY))
            ], 'CONFIG_FAIR_GROUP_SCHED'),
            FieldGroup([
                Field('h_load', Int(size = None, signed = False)),
                Field('last_h_load_update', Int(size = 8, signed = False)),
                Field('h_load_next', Pointer(SCHED_ENTITY))
            ],'CONFIG_FAIR_GROUP_SCHED'),
            FieldGroup([
                Field('rq', Pointer()), #struct rq
                Field('on_list', Int()),
                Field('leaf_cfs_rq_list', _ListHead()),
                Field('tg', Pointer()) #struct task_group
            ], 'CONFIG_FAIR_GROUP_SCHED'),
            FieldGroup([
                Field('runtime_enabled', Int()),
	            Field('runtime_expires', Int(size = 8, signed = False)),
	            Field('runtime_remaining', Int(size = 8, signed = True)),
	            Field('throttled_clock',Int(size = 8, signed = False)),
                Field('throttled_clock_task', Int(size = 8, signed = False)),
	            Field('throttled_clock_task_time', Int(size = 8, signed = False)),
	            Field('throttled', Int()),
                Field('throttle_count', Int()),
                Field('throttle_uptodate', Int()),
                Field('throttled_list', LIST_HEAD)
            ],'CONFIG_CFS_BANDWIDTH')
        ])
CFSRQ = _CFSRQ()

class _RCU_SPECIAL(_Union):
    def __init__(self, name):
        super().__init__(name, [
            _Struct('b', [
                FieldGroup([
                    Field('blocked', Int(size=1, signed=False)),
                    Field('need_qs', Int(size=1, signed=False)),
                    Field('exp_need_qs', Int(size=1, signed=False)),
                    Field('pad', Int(size=1, signed=False))
                ])
            ]),
            Int(size=4, signed=False)
        ])
RCU_READ_UNLOCK_SPECIAL=_RCU_SPECIAL('rcu_read_unlock_special')

class _TaskStruct(_Struct):
    def __init__(self):
        super().__init__('task_struct', [
            FieldGroup([
                Field('state', Int(size = None)), # -1 unrunnable, 0 runnable, >0 stopped
	            Field('stack', Pointer()),
                Field('usage', ATOMIC),
                Field('flags', Int(signed = False)), #per process flags, defined below
                Field('ptrace', Int(signed = False))
            ]),
            FieldGroup([
                Field('wake_entry', LLIST_NODE),
                Field('on_cpu', Int()),
                Field('wakee_flips', Int(signed = False)),
                Field('wakee_flip_decay_ts', Int(size = None, signed = False)),
                Field('last_wakee', Pointer(self)),
                Field('wake_cpu', Int())
            ], 'CONFIG_SMP'),
            FieldGroup([
                Field('on_rq', Int()),
                Field('prio', Int()),
                Field('static_prio', Int()),
                Field('normal_prio', Int()),
                Field('rt_priority', Int(signed = False)),
                Field('sched_class', Pointer()), #struct sched_class*
                Field('se', SCHED_ENTITY),
                Field('rt', SCHED_RT_ENTITY)
            ]),
            FieldGroup([
                Field('task_group', Pointer()) #struct task_group*
            ], 'CONFIG_CGROUP_SCHED'),
            FieldGroup([
                Field('dl', SCHED_DL_ENTITY)
            ]),
            FieldGroup([
                Field('preempt_notifiers', HLIST_HEAD)
            ], 'CONFIG_PREEMPT_NOTIFIERS'),
            FieldGroup([
                Field('btrace_seq', Int(signed = False))
            ], 'CONFIG_BLK_DEV_IO_TRACE'),
            FieldGroup([
                Field('policy', Int(signed = False)),
                Field('nr_cpus_allowed', Int()),
                Field('cpus_allowed', CPUMASK)
            ]),
            FieldGroup([
                Field('rcu_read_lock_nesting', Int()),
                Field('rcu_read_unlock_special', RCU_READ_UNLOCK_SPECIAL),
                Field('rcu_node_entry', LIST_HEAD),
                Field('rcu_blocked_node', Pointer()) #struct rcu_node*
            ], 'CONFIG_PREEMPT_RCU'),
            FieldGroup([
                Field('rcu_tasks_nvcsw', Int(size = None, signed = False)),
                Field('rcu_tasks_holdout', Bool()),
                Field('rcu_tasks_holdout_list', LIST_HEAD),
                Field('rcu_tasks_idle_cpu', Int())
            ], 'CONFIG_TASKS_RCU'),
            FieldGroup([
                Field('sched_info', SCHED_INFO)
            ], 'CONFIG_SCHED_INFO'),
            FieldGroup([
                Field('tasks', LIST_HEAD)
            ])
        ])
TASK_STRUCT = _TaskStruct()

def test_list_head(context, address, offset):
    # Assumes that the address is a valid list head
    # prev_pointer = context.read_pointer(address)
    # prev_task = prev_pointer + offset

    # results = TASK_STRUCT.test(context, prev_task, True)

    # if (len(results) == 0):
    #     return False

    return True
