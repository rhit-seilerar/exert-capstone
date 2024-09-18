# Day 1 (Introduction to PANDA)
#
# Template for exercise 5, parts ...
#
# Exercise 5: Hooks magic
#
# In exercise 4 we saw that `maxdem` was engaged in some odd behavior,
# including opening password-ish files and loading the libgcrypt
# library. Add analysis to that PANDA script to observe what
# encryption function(s) are being employed.  And then iterate and dig
# deper to to see what data is being encrypted.


from pandare import Panda
panda = Panda(generic="x86_64")

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

    cmdname = panda.ffi.string(auxv.argv[0]).decode()
    if ("maxdem" in cmdname):

        # Note: we'll use the machinery of ex 4 to limit
        # the application of these expensive introspections to
        # just `maxdem`
        
        # Part 1. Use `@panda.hook_symbol` to intercept *all* functions
        # actually called by `libgcrypt`.
        @panda.hook_symbol(AAA, BBB)
        def hook_libgcrypt(CCC):
            # Part 2. 
            # print out the name of the fn here
            print(...)
    
        # Part 3. Iterate, now that you know the name of the
        # encryption fn being called.  Uncomment this decorator
        # (enabling the hook).  Then fill in the args to that
        # correctly.  Then proceed to parts 4 and 5, below.
        #@panda.hook_symbol(DDD, EEE)
        def hook_encrypt(...):
            # Part 4. Look at the type signature to that encryption function and add
            # code here to get the arg that is the pointer to the buffer of
            # plaintext
            ..., ptr, .. = panda.arch.get_args(...)
            # Part 5. Read that buffer out of guest using `panda.virtual_memory_read`
            buf = panda.virtual_memory_read(..., ptr, ...)
            print("Saw plaintext buf=[%s] passed to encrytion fn")
            

panda.run()
