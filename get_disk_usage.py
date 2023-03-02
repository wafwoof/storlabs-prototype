import shutil

total, used, free = shutil.disk_usage("/")
# convert all to GB
total = total // (2**30)
used = used // (2**30)
free = free // (2**30)

print(f"Total: {total} GB")
print(f"Used: {used} GB")
print(f"Free: {free} GB")