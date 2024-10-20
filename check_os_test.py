import platform
# since startup and attach to container use diff commands depending on OS, we decided to separate those commands into a new file
# then we have the exert filter out which commands to use based on the system detected. This is a demonstration on how to get the system name and work with it.
# this will hopefully print out the name of the platform and we can do stuff with it
sys_name_thing = platform.uname()
print(sys_name_thing.system)
if sys_name_thing.system == "Windows":
    print("You are on Windows!")

