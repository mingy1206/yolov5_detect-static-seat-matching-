import math

# Read bounding boxes from a file for a specific class
def read_bounding_boxes(file_path, target_class=0):
    with open(file_path, 'r') as file:
        boxes = [list(map(float, line.split()[1:])) for line in file.readlines() if
                 int(line.split()[0]) == target_class]
    return boxes



# Convert bounding box format from (center_x, center_y, width, height) to (xmin, ymin, xmax, ymax)
def convert_box_format(box):
    x, y, w, h = box
    left = x - w / 2
    top = y - h / 2
    right = x + w / 2
    bottom = y + h / 2
    return left, top, right, bottom



# Calculate Euclidean distance between two boxes
def calculate_distance(box1, box2):
    return math.sqrt((box1[0] - box2[0]) ** 2 + (box1[1] - box2[1]) ** 2)
# Calculate Intersection over Union (IoU) for two boxes
def calculate_iou(box1, box2):
    box1 = convert_box_format(box1)
    box2 = convert_box_format(box2)

    inter_left = max(box1[0], box2[0])
    inter_top = max(box1[1], box2[1])
    inter_right = min(box1[2], box2[2])
    inter_bottom = min(box1[3], box2[3])

    if inter_right < inter_left or inter_bottom < inter_top:
        return 0.0

    inter_area = (inter_right - inter_left) * (inter_bottom - inter_top)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    iou = inter_area / float(box1_area + box2_area - inter_area)
    return iou

# Match YOLO detected boxes with seat boxes
def match_boxes(file_yolo, file_seat):
    yolo_boxes = read_bounding_boxes(file_yolo)
    seat_boxes = read_bounding_boxes(file_seat)

    matches = []
    for i, yolo_box in enumerate(yolo_boxes):
        best_match = (-1, 0)  # (index, IoU)
        for j, seat_box in enumerate(seat_boxes):
            iou = calculate_iou(yolo_box, seat_box)

            if iou > best_match[1]:  # Update if a better IoU is found
                best_match = (j, iou)

        if best_match[1] > 0:  # If there's an overlap
            # Find the closest box using Euclidean distance
            closest_distance = float('inf')
            closest_seat_box_index = -1
            for j, seat_box in enumerate(seat_boxes):
                distance = calculate_distance(yolo_box, seat_box)

                if distance < closest_distance:
                    closest_distance = distance
                    closest_seat_box_index = j

            matches.append((i, closest_seat_box_index))
        else:  # If no overlap, find the closest box based on Euclidean distance
            closest_distance = float('inf')
            closest_seat_box_index = -1
            for j, seat_box in enumerate(seat_boxes):
                distance = calculate_distance(yolo_box, seat_box)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_seat_box_index = j
            matches.append((i, closest_seat_box_index))

    return matches