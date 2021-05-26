import functools
import os
import cv2
import matplotlib.pyplot as plt


def get_iou(bb1, bb2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters
    ----------
    bb1 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x, y) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner

    Returns
    -------
    float
        in [0, 1]
    """
    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the intersection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou


def convert_xywh_to_bb(coords):
    x, y, w, h = coords
    return dict({
        "x1": x,
        "y1": y,
        "x2": x + w,
        "y2": y + h
    })


# single class implementation
def calculate_confusion_matrix(grounds, preds, threshold=0.3):
    if len(grounds) == 0 or preds == 0:
        return (0, 0, 0,), []

    grounds = map(convert_xywh_to_bb, grounds)
    preds = map(convert_xywh_to_bb, preds)
    sequence = []

    TP = FP = FN = 0

    for ground in grounds:
        candidates = []
        for prd in preds:
            p = get_iou(ground, prd)
            if p > 0:
                candidates.append(p)
        upper_candidates = [i for i in candidates if i >= threshold]  # filter
        TP += len(upper_candidates[:1])
        FP += len(candidates) - 1 + len(upper_candidates[1:])
        if upper_candidates == 0:
            FN += 1
        sequence.append((TP, FP, FN))
    return (TP, FP, FN), sequence


def calculate_precision(cf_matrix):
    (TP, FP, FN) = cf_matrix
    if TP + FP == 0:
        return 0
    return TP / (TP + FP)


def calculate_recall(cf_matrix):
    (TP, FP, FN) = cf_matrix
    if TP + FN == 0:
        return 0
    else:
        return TP / (TP + FN)


# Area under curve implementation
def calculateAP(pre_rec_s):
    r_v = 0
    for i in range(1, len(pre_rec_s)):
        pr, rc = pre_rec_s[i]
        prev_pr, prev_rc = pre_rec_s[i - 1][1]
        new_area = max(pr, prev_pr) * (rc - prev_rc)
        r_v += new_area
    return r_v


def reader():
    ground_path = 'groundtruths'
    detect_path = 'detections'

    grounds = []
    detects = []

    for (dirpath, dirnames, filenames) in os.walk(ground_path):
        if len(dirnames) == 0:
            file_paths = [os.path.join(dirpath, f_name) for f_name in filenames]
            for path in file_paths:
                with open(path, 'r') as f:
                    for line in f:
                        grounds.append([float(i) for i in line.split(' ')[1:]])

    for (dirpath, dirnames, filenames) in os.walk(detect_path):
        if len(dirnames) == 0:
            file_paths = [os.path.join(dirpath, f_name) for f_name in filenames]
            for path in file_paths:
                with open(path, 'r') as f:
                    for line in f:
                        detects.append([float(i) for i in line.split(' ')[2:]])

    return grounds, detects


if __name__ == '__main__':
    grounds, detects = reader()
    m, s = calculate_confusion_matrix(grounds, detects, 0.3)

    final_precision = calculate_precision(m)
    final_recall = calculate_recall(m)

    # for graphing curves
    sequence_precision = [calculate_precision(i) for i in s]
    sequence_recall = [calculate_recall(i) for i in s]

    graphing_points = [i for i in zip(sequence_precision, sequence_recall)]
    graphing_points.sort(key=lambda k: k[1])

    AP = calculateAP(graphing_points)

    print(f"Precision: {final_precision}, Recall: {final_recall}, AP: {AP}")

    graphing_points = [(0, 1), (1, 2)]
    print(graphing_points)
    plt.plot([i[0] for i in graphing_points], [i[1] for i in graphing_points])

    plt.title('Precision x Recall Curves')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.show()

    #
    # (x, y, w, h) = coords
    # img = cv2.imread('WIDER_val/images/0--Parade/0_Parade_Parade_0_194.jpg')
    # img = cv2.resize(img, (1000, 1000))
    # trans = convert_xywh_to_bb(coords)
    # trans_2 = convert_xywh_to_bb(coords_2)
    #
    # image = cv2.rectangle(img, (trans['x1'], trans['y1']), (trans['x2'], trans['y2']), (255, 0, 0), thickness=2)
    # image = cv2.rectangle(image, (trans_2['x1'], trans_2['y1']), (trans_2['x2'], trans_2['y2']), (0, 255, 0),
    #                       thickness=2)
    #
    # cv2.imshow('test', image)
    # cv2.waitKey(10000)
    # cv2.destroyAllWindows()
