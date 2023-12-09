import os
from pathlib import Path
from collections import Counter

# Function to read bounding boxes from a file for a specific class
def read_bounding_boxes(file_path, target_class=0):
    with open(file_path, 'r') as file:
        boxes = [list(map(float, line.split()[1:])) for line in file.readlines() if
                 int(line.split()[0]) == target_class]
    return len(boxes)

# Directory containing text files to analyze
directory_path = 'runs/detect/texts'

# Get a list of all text files in the directory
text_files = [file for file in Path(directory_path).glob('*.txt')]

# Initialize a Counter to count instances of class 0
class_0_counts = Counter()

# Initialize a variable to store the path of the last file with the most common count
last_file_with_most_common_count = None

# Iterate through each text file and count instances of class 0
for file_path in text_files:
    count_class_0 = read_bounding_boxes(file_path)
    class_0_counts[count_class_0] += 1

    # Check if this file has the most common count
    if count_class_0 == class_0_counts.most_common(1)[0][0]:
        last_file_with_most_common_count = file_path

# Find the most common count
most_common_count = class_0_counts.most_common(1)[0][0]

# Print the most common count and the path of the last file with that count
print(f"The most common count of class 0 instances is: {most_common_count}")
print(f"The path of the last file with this count is: {last_file_with_most_common_count}")
