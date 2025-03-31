import sys
from exert.utilities import version as ver
from exert.usermode import plugin

KERNEL_ADDRESS = []

def empty_callback(panda, cpu): # pragma: no cover
    return

def get_data_addresses(panda, cpu): # pragma: no cover
    magic = panda.arch.get_arg(cpu, 0, convention='syscall')
    string_address = panda.arch.get_arg(cpu, 1, convention='syscall')
    assert magic == 204
    address_string = panda.read_str(cpu, string_address)

    address_parts = address_string.split()

    address = []
    for part in address_parts:
        if part.find('x') != -1:
            address.append(part)

    assert len(address) == 2
    global KERNEL_ADDRESS 
    KERNEL_ADDRESS = address

def get_osi_info(kernel, arch, version):
    version_supported = False

    ver_entry = ver.version_from_string(version)

    min_ver = ver.Version(4,4,99)
    max_ver = ver.Version(4,4,101)
    if (arch in ['armv4l', 'armv5l', 'armv6l', 'armv7l', 'x86_64', 'i386', 'aarch64']):
        if(ver.compare_version(ver_entry, min_ver) and ver.compare_version(max_ver, ver_entry)):
            version_supported = True

            dmesg_prog = ''
            if (arch in ['armv4l', 'armv5l', 'armv6l', 'armv7l']):
                dmesg_prog = 'dmesg-armv5l'
            else:
                dmesg_prog = 'dmesg-' + arch 

            plugin.run(arch=arch, generic=False, kernel=kernel,
                       usermode=dmesg_prog, command='./user_prog',
                       callback = empty_callback, hypercall_callback=get_data_addresses)
            
            print(KERNEL_ADDRESS)

    if not version_supported:
        print("Version not supported")

if __name__ == '__main__':
    get_osi_info(sys.argv[1], sys.argv[2], sys.argv[3])
