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
    matched_seat_boxes = set()  # 이미 매치된 seat_box 인덱스를 저장

    matches = []
    for i, yolo_box in enumerate(yolo_boxes):
        best_match = (-1, float('inf'))  # (index, distance)
        for j, seat_box in enumerate(seat_boxes):
            iou = calculate_iou(yolo_box, seat_box)

            # IoU가 0이 아니고, 해당 seat_box가 아직 매치되지 않았다면
            if iou > 0 and j not in matched_seat_boxes:
                distance = calculate_distance(yolo_box, seat_box)
                if distance < best_match[1]:  # 더 가까운 seat_box를 찾으면 업데이트
                    best_match = (j, distance)

        # 매치된 seat_box가 있다면, matched_seat_boxes에 추가
        if best_match[0] != -1:
            matched_seat_boxes.add(best_match[0])
            matches.append((i, best_match[0]))
        else:  # 매치되지 않은 경우
            matches.append((i, None))

    return matches