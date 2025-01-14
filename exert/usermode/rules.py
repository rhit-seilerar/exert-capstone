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

    def test_all(self, context, addresses):
        passing = set()
        for field in self.fields:
            passing |= field.test_all(context, addresses)
        return passing

    def __str__(self):
        fields_str = ', '.join(str(f) for f in self.fields)
        cond_str = 'None' if self.condition is None else f"'{self.condition}'"
        return f'FieldGroup([{fields_str}], {cond_str})'

class Struct(Rule):
    def __init__(self, name, field_groups):
        super().__init__()
        self.name = name
        self.field_groups = field_groups

    def _get_key(self):
        groups_str = ', '.join([str(g) for g in self.field_groups])
        return f"Struct('{self.name}', [{groups_str}])"

    def _test(self, context, address):
        passing = {address}
        for group in self.field_groups:
            if group.condition:
                passing |= group.test_all(context, passing)
            else:
                passing = group.test_all(context, passing)
        return passing

class _Struct(Struct):
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
            Field('util_avg', Int(size = None, signed = False)),
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
            Field('nr_wakeups_idle', Int(size = 8, signed = False)),
        ])])
SCHED_STATISTICS = _SchedStatistics()

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

class _KTimeT(_Struct): #supposed to be a union
    def __init__(self):
        super().__init__('timerqueue_node', [
            FieldGroup([
                Field('tv64', Int(size = 8))
            ])
        ])
KTIME_T = _KTimeT()

class _HListHead(_Struct): #supposed to be a union
    def __init__(self):
        super().__init__('hlist_head', [
            FieldGroup([
	        Field('first', Pointer()) #struct hlist_node *first;
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

class _HRTimer(_Struct):
    def __init__(self):
        super().__init__('hrtimer', [
            FieldGroup([
                Field('node', TIMERQUEUENODE),
                Field('_softexpires', KTIME_T),
                Field('function', Pointer()), # enum hrtimer_restart		(*function)(struct hrtimer *);
                Field('base', Pointer()), #struct hrtimer_clock_base	*base;
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
            # TODO What if there are more than 64?
            # maybe we use some kind of callback to generate more?
            # Or just make it a user parameter
            Field('bits', Array(Int(size = None, signed = False), 1, 64))
        ])])
CPUMASK = _CpuMask()

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
                #TODO this should be 'union rcu_special'
                Field('rcu_read_unlock_special', Int(signed = False)),
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
