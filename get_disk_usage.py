import shutil

total, used, free = shutil.disk_usage("/")

# convert to percentage
usage_percentage = int(used/total * 1000)
print(f"Usage: {used}/{total} ({usage_percentage}%)")