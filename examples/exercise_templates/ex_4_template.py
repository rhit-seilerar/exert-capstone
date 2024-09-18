# Day 1 (Introduction to PANDA)
#
# Template for exercise 4, parts 1-4
#
# Exercise 4: Syscalls, hooks, and osi for deeper analysis  
#
# In exercise 3, we learned that a mysterious process named "maxdem"
# is running after `benew` runs.  Here, we will investigate that
# program, logging the system calls it runs and some of their
# arguments.
#
# lessons: syscalls_logger, hooks, and get_mappings (osi)


from pandare import Panda
panda = Panda(generic="x86_64")

# Part 1. Add a single line of code here to load `syscalls_logger`
# plugin and to pass it one argument:
#   target = maxdem      -- restrict to just this process
panda.load_plugin(...)

# Look how many things we can get the guest driver to do!
@panda.queue_blocking
def guest_driver():
    panda.revert_sync("root")
    cmds = ["rm /usr/bin/apt* /usr/bin/dpkg",
            "dhclient -v",
            "wget http://leet.mit.edu:9000/benew",
            "chmod +x benew",
            "./benew"]
    for cmd in cmds:
        print("cmd=[%s]" % cmd)
        print(panda.run_serial_cmd(cmd, no_timeout=True))

    panda.end_analysis()


@panda.ppp('proc_start_linux', 'on_rec_auxv')
def on_recv(cpu, tb, auxv):
    print("-" * 40)
    print("on_recv: ", end="")
    for idx in range(auxv.argc):
        this_arg_cstring = auxv.argv[idx]
        arg = panda.ffi.string(this_arg_cstring).decode()
        print(arg + " ", end="")
    print()

    # Part 2. Use a field of auxv to get command name and then 
    # arrange for the following to only run for process `maxdem`
    cmdname = SOME_PANDA_FN_TO_GET_GUEST_STRING(auxv.FIELD_THAT_IS_CMD_NAME).decode()
    if "maxdem" in cmdname:
    
        # Part 3. Use a field of auxv, here, to hook entry point 
        # of `maxdem`
        entry = auxv.FIELD_THAT_IS_ENTRY
        print("entry point for maxdem is %x" % auxv.entry)
        @panda.hook(entry)
        def hook_entry(cpu, tb, h):
            # Part 4. use `panda.get_mappings() to iterate over
            # libraries loaded by maxdem and print out their names
            ...

        
panda.run()
