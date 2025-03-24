from dataclasses import dataclass

@dataclass
class Version:
    x: int
    y: int
    z: int

def version_from_string(entry):
    number_string = input.split('-')[0]
    nums = number_string.split('.')
    v = Version(int(nums[0]), int(nums[1]), int(nums[2]))
    return v

def compare_version(entry, target):
    if entry.x > target.x:
        return True
    if entry.x == target.x:
        if entry.y > target.y:
            return True
        if entry.y == target.y and entry.z >= target.z:
            return True
    return False
