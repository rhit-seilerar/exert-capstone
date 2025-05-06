from pandare import Panda
from exert.usermode import plugin
from exert.utilities.types.multi_arch import CPUState

def process_lister(panda: Panda, cpu: CPUState) -> None:
    processes_dict = panda.get_processes_dict(cpu)
    for key, value in processes_dict.items():
        print(f'Process {key} is called {value['name']}')

    print(f'There are {len(processes_dict)} total processes')

def run_osi_with_arm() -> None:
    plugin.run('arm', callback=process_lister)
