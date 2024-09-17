from pandare import Panda
panda = Panda(generic='i386')
blocks = 0
@panda.cb_before_block_exec
def before_block_execute(cpustate, transblock):
    global blocks
    blocks += 1

@panda.queue_blocking
def run_cmd():
    panda.revert_sync("root")
    print(panda.run_serial_cmd("uname -a"))
    panda.end_analysis()

panda.run()
print("Finished. Saw a total of {} basic blocks during execution".format(blocks))

