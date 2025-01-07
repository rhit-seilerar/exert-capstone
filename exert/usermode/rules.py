class Rule:
    _cache = {}

    def ctest(self, context):
        return self.test(context, True)

    def test(self, context, clear_cache = False):
        if clear_cache:
            Rule._cache.clear()

        # For efficiency, we memoize the test() method by caching results
        pair = (self, context.address)
        if pair in Rule._cache:
            return Rule._cache[pair]

        # We may end up testing ourselves, so temporarily store True to pass the above check
        Rule._cache[pair] = True
        # print(f'Testing {self}')
        result = self._test(context)
        Rule._cache[pair] = result
        return result

    def _test(self, context):
        return True

    # def __str__(self):
    #     return 'Rule()'

class Int(Rule):
    def __init__(self, value = None, size = 4, signed = True):
        self.size = size
        self.signed = signed
        self.value = value

    def _test(self, context):
        context.suspend()
        size = context.word_size if self.size is None else self.size
        val = context.next_int(size, self.signed)
        return context.apply(self.value is None or val == self.value)
    # def __str__(self):
    #     return f'Int({self.value}, {self.size}, {self.signed})'

class Bool(Int):
    def __init__(self, value = None):
        super().__init__(value, size = 1)

class Pointer(Rule):
    def __init__(self, rule = None):
        self.rule = rule

    def _test(self, context):
        context.suspend()

        # Test if the pointer points to a valid memory address
        pointer = context.next_pointer()
        data = context.read(pointer, 0)
        if pointer != 0 and data is None:
            print("Pointer is invalid: " + str(context.panda.buf))
            return context.apply(False)

        print("Pointer is valid")
        # Test futher rules against the found data
        new_ctx = context.copy(pointer)
        return context.apply(self.rule is None or self.rule.test(new_ctx))

    # def __str__(self):
    #     return f'Pointer({str(self.rule)})'

class Field(Rule):
    def __init__(self, name, rule):
        self.name = name
        self.rule = rule

    def _test(self, context):
        return self.rule.test(context)

    # def __str__(self):
    #     return f'Field(\'{self.name}\', {str(self.rule)})'

class FieldGroup(Rule):
    def __init__(self, fields, optional=False):
        self.fields = fields
        self.optional = optional

    def _test(self, context):
        context.suspend()
        for field in self.fields:
            if not field.test(context):
                return context.apply(False)
        return context.apply(True)

    # def __str__(self):
    #     return f'FieldGroup([{", ".join(str(f) for f in self.fields)}], {self.optional})'

class Struct(Rule):
    def __init__(self, name, field_groups):
        self.name = name
        self.field_groups = field_groups

    def _test(self, context):
        def helper(context, groups):
            if len(groups) == 0:
                return True
            context.suspend()
            group = groups[0]
            context_copy = context.copy()
            passes = group.test(context) and helper(context, groups[1:])
            if group.optional and helper(context_copy, groups[1:]):
                passes = True
                context = context_copy
            return context.apply(passes)
        return helper(context, self.field_groups)

    # def __str__(self):
    #     return f'Struct(\'{self.name}\', [{", ".join(str(g) for g in self.field_groups)}])'

class _Atomic(Struct):
    def __init__(self):
        super().__init__('atomic_t', [FieldGroup([
            Field('counter', Int())
        ])])
ATOMIC = _Atomic()

class _LoadWeight(Struct):
    def __init__(self):
        super().__init__('load_weight', [FieldGroup([
            Field('weight', Int(size = None, signed = False)),
            Field('inv_weight', Int(signed = False))
        ])])
LOAD_WEIGHT = _LoadWeight()

class _RBNode(Struct):
    def __init__(self):
        super().__init__('rb_node', [FieldGroup([
            Field('__rb_parent_color', Int(size = None, signed = False)),
            Field('rb_right', Pointer(self)),
            Field('rb_left', Pointer(self))
        ])])
RB_NODE = _RBNode()

class _LListNode(Struct):
    def __init__(self):
        super().__init__('llist_node', [FieldGroup([
            Field('next', Pointer(self))
        ])])
LLIST_NODE = _LListNode()

class _SchedAvg(Struct):
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

class _ListHead(Struct):
    def __init__(self):
        super().__init__('list_head', [FieldGroup([
            Field('next', Pointer(self)),
            Field('prev', Pointer(self))
        ])])

    def _test(self, context):
        context.suspend()
        if not super()._test(context):
            return context.apply(False)
        context.apply(False)

        # Validate that neighboring list heads maintain a full loop
        context.suspend()
        address = context.address

        next_pointer = context.next_pointer()
        next_prev_address = next_pointer + context.word_size
        next_prev_pointer = context.read_pointer(next_prev_address)

        prev_pointer = context.next_pointer()
        prev_next_address = prev_pointer + 0
        prev_next_pointer = context.read_pointer(prev_next_address)

        valid = next_prev_pointer == address and prev_next_pointer == address
        return context.apply(valid)
LIST_HEAD = _ListHead()

class _SchedInfo(Struct):
    def __init__(self):
        super().__init__('sched_info', [FieldGroup([
                Field('pcount', Int(size = None, signed = False)),
                Field('run_delay', Int(size = 8, signed = False)),
                Field('last_arrival', Int(size = 8, signed = False)),
                Field('last_queued', Int(size = 8, signed = False))
        ])])
SCHED_INFO = _SchedInfo()

class _SchedStatistics(Struct):
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

class _SchedEntity(Struct):
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
            FieldGroup([ #ifdef CONFIG_SCHEDSTATS
                Field('statistics', SCHED_STATISTICS)
            ], True),
            FieldGroup([ #ifdef CONFIG_FAIR_GROUP_SCHED
                Field('depth', Int()),
                Field('parent', Pointer(self)),
                Field('cfs_rq', Pointer()), #struct cfs_rq
                Field('my_q', Pointer()) #struct cfs_rq
            ], True),
            FieldGroup([ #ifdef CONFIG_SMP
	            Field('avg', SCHED_AVG)
            ], True)
        ])
SCHED_ENTITY = _SchedEntity()

class _SchedRTEntity(Struct):
    def __init__(self):
        super().__init__('sched_rt_entity', [
            FieldGroup([
                Field('run_list', LIST_HEAD),
                Field('timeout', Int(size = None, signed = False)),
                Field('watchdog_stamp', Int(size = None, signed = False)),
                Field('time_slice', Int(signed = False)),
                Field('back', Pointer(self))
            ]),
            FieldGroup([ #ifdef CONFIG_RT_GROUP_SCHED
                Field('parent', Pointer(self)),
                Field('rt_rq', Pointer()), #struct rt_rq*
                Field('my_q', Pointer())  #struct rt_rq*
            ], True)
        ])
SCHED_RT_ENTITY = _SchedRTEntity()

class _KTimeT(Struct): #supposed to be a union
    def __init__(self):
        super().__init__('timerqueue_node', [
            FieldGroup([
                Field('tv64', Int(size = 8))
            ])
        ])
KTIME_T = _KTimeT()

class _HListHead(Struct): #supposed to be a union
    def __init__(self):
        super().__init__('hlist_head', [
            FieldGroup([
	        Field('first', Pointer()) #struct hlist_node *first;
            ])
        ])
HLIST_HEAD = _HListHead()

class _TimerQueueNode(Struct):
    def __init__(self):
        super().__init__('timerqueue_node', [FieldGroup([
            Field('node', RB_NODE),
            Field('expires', KTIME_T)
        ])])
TIMERQUEUENODE = _TimerQueueNode()

class _HRTimer(Struct):
    def __init__(self):
        super().__init__('hrtimer', [
            FieldGroup([
                Field('node', TIMERQUEUENODE),
                Field('_softexpires', KTIME_T),
                Field('function', Pointer()), # enum hrtimer_restart		(*function)(struct hrtimer *);
                Field('base', Pointer()), #struct hrtimer_clock_base	*base;
                Field('state', Int(size = 1, signed = False)),
                Field('is_rel', Int(size = 1, signed = False))
            ])
            #TODO
        #     FieldGroup([ #ifdef CONFIG_TIMER_STATS
        # int				start_pid;
        # void				*start_site;
        # char				start_comm[16];
        #     ], True)
        ])
HRTIMER = _HRTimer()

class _SchedDLEntity(Struct):
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

class _TaskStruct(Struct):
    def __init__(self):
        super().__init__('task_struct', [
            FieldGroup([
                Field('state', Int(size = None)), # -1 unrunnable, 0 runnable, >0 stopped
	            Field('stack', Pointer()),
                Field('usage', ATOMIC),
                Field('flags', Int(signed = False)), #per process flags, defined below
                Field('ptrace', Int(signed = False))
            ]),
            FieldGroup([ #ifdef CONFIG_SMP
                Field('wake_entry', LLIST_NODE),
                Field('on_cpu', Int()),
                Field('wakee_flips', Int(signed = False)),
                Field('wakee_flip_decay_ts', Int(size = None, signed = False)),
                Field('last_wakee', Pointer(self)),
                Field('wake_cpu', Int())
            ], True),
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
            FieldGroup([ #ifdef CONFIG_CGROUP_SCHED
                Field('task_group', Pointer()) #struct task_group*
            ], True),
            FieldGroup([
                Field('dl', SCHED_DL_ENTITY)
            ]),
            FieldGroup([ #ifdef CONFIG_PREEMPT_NOTIFIERS
                Field('preempt_notifiers', HLIST_HEAD)
            ], True),
            FieldGroup([ #ifdef CONFIG_BLK_DEV_IO_TRACE
                Field('btrace_seq', Int(signed = False))
            ], True),
            FieldGroup([
                Field('policy', Int(signed = False)),
                Field('nr_cpus_allowed', Int()),
                #TODO # cpumask_t cpus_allowed;
            ]),
            FieldGroup([ #ifdef CONFIG_PREEMPT_RCU
                Field('rcu_read_lock_nesting', Int()),
                #TODO #union rcu_special rcu_read_unlock_special;
                Field('rcu_node_entry', LIST_HEAD),
                Field('rcu_blocked_node', Pointer()) #struct rcu_node*
            ], True),
            FieldGroup([ #ifdef CONFIG_TASKS_RCU
                Field('rcu_tasks_nvcsw', Int(size = None, signed = False)),
                Field('rcu_tasks_holdout', Bool()),
                Field('rcu_tasks_holdout_list', LIST_HEAD),
                Field('rcu_tasks_idle_cpu', Int())
            ], True),
            FieldGroup([ #ifdef CONFIG_SCHED_INFO
                Field('sched_info', SCHED_INFO)
            ], True),
            FieldGroup([
                Field('tasks', LIST_HEAD)
            ])
        ])
TASK_STRUCT = _TaskStruct()
