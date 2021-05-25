import os

target_path = 'groundtruths'
mirror_path = 'detections'

files = []
for (dirpath, dirnames, filenames) in os.walk(target_path):
    if len(dirnames) == 0:
        files.extend([f_name for f_name in filenames])

# print(files[0])

for filename in files:
    mirror = os.path.join(mirror_path, filename)
    if os.path.exists(mirror) is False:
        target = os.path.join(target_path, filename)
        os.remove(target)
