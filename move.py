import os
from pathlib import Path
from collections import Counter

from calculate import read_bounding_boxes, match_boxes



def count_matched_boxes(file_path, file_seat, target_class=0):
    yolo_boxes = read_bounding_boxes(file_path, target_class)
    matched_boxes = match_boxes(file_path, file_seat)
    # class0(사람)만 측정
    return sum(1 for match in matched_boxes if match[1] is not None)

# path
directory_path = 'runs/detect/texts'
file_seat = 'seat.txt'  # Path to the seat.txt file

# 모든 text 파일 실행
text_files = [file for file in Path(directory_path).glob('*.txt')]

# Initialize
class_0_counts = Counter()

# Initialize
last_file_with_most_common_count = None

# class 0(사람) instance 계산
for file_path in text_files:
    count_class_0 = count_matched_boxes(file_path, file_seat, target_class=0)
    class_0_counts[count_class_0] += 1

    if count_class_0 == class_0_counts.most_common(1)[0][0]:
        last_file_with_most_common_count = file_path

# 제일 많이 중복 되는 instance의 경우
most_common_count = class_0_counts.most_common(1)[0][0]

# 결과 출력
print(f"The most common count of matched class 0 instances is: {most_common_count}")
print(f"The path of the last file with this count is: {last_file_with_most_common_count}")