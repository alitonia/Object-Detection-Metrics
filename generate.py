from os import walk
import os


def change_ext(file, new_ext):
    filename, file_extension = os.path.splitext(file)
    return filename + '.' + new_ext


def next_step(step: str, l: list):
    i = l.index(step)
    return l[(i + 1) % len(l)]


positive_data = []
negative_data = []

# wider face images
with open('wider_face_split/wider_face_val_bbx_gt.txt', 'r') as f:
    name = ''
    items = 0
    item_count = 0
    bounding_data = []
    steps = ['name', 'count', 'box']
    step = steps[0]
    skip_box = False
    o = dict()

    for (i, line) in enumerate(f):
        if item_count == items and step == steps[-1]:
            items = 0
            item_count = 0
            name = ''
            o['box'] = bounding_data
            if o['items'] == 0:
                negative_data.append(o)
            else:
                positive_data.append(o)
            o = dict()
            bounding_data = []
            step = next_step(step, steps)
            # done
            # break

        if step == steps[0]:
            name = line[:-1]
            step = next_step(step, steps)
            o['name'] = os.path.split(name)[1]
        elif step == steps[1]:
            items = int(line)
            o['items'] = items
            if items == 0:
                items = 1
            step = next_step(step, steps)

        else:
            x, y, w, h, *_ = line.split(' ')
            bounding_data.extend([x, y, w, h])
            item_count += 1

print(f"Total: {len(positive_data)}")
with open('temp.log', 'w') as f:
    f.write(str(len(positive_data)))

path = 'groundtruths'
for thing in positive_data:
    file_name = change_ext(os.path.join(path, thing['name']), 'txt')
    with open(file_name, 'w') as f:
        label = 'face'
        for (i, x) in enumerate(thing['box']):
            if i % 4 == 0:
                f.write(f"{label} {x}")
            else:
                f.write(f" {x}")
            if i % 4 == 3:
                f.write('\n')
