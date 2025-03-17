from dataclasses import dataclass

@dataclass
class Version:
    x: int
    y: int
    z: int

def version_from_string(input):
    number_string = input.split('-')[0]
    nums = number_string.split('.')
    v = Version(int(nums[0]), int(nums[1]), int(nums[2]))
    return v

def compare_version(entry, target):
    if(entry.x > target.x):
        return True
    elif(entry.x == target.x):
        if(entry.y > target.y):
            return True
        elif(entry.y == target.y and entry.z >= target.z):
            return True
    return False

def compare_version_max(entry, target):
    return compare_version(target, entry)
