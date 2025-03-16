from dataclasses import dataclass

@dataclass
class Version:
    v0: int
    v1: int
    v2: int


def compareVersion(entry, target): #check if input version is >= target
    print(f"Entry = {entry} ")
    print(f"Target = {target} ")

    if(entry.v0 >= target.v0 and entry.v1 >= target.v1 and entry.v2 >= target.v2):
        return True
    return False

def compareVersionMax(entry, target):
    return compareVersion(target, entry)

va = Version(1,2,5)
vb = Version(1,3,2)
print(va)
print(compareVersion(va,vb)) # should print False
print(compareVersionMax(va,vb)) # should print True