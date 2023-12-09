import subprocess
import os
import shutil
from pathlib import Path
from calculate import match_boxes

def clear_directory(directory):
    if directory.exists() and directory.is_dir():
        shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)

def run_yolov5_detection():
    base_dir = Path('C:\\Users\\gram15\\smartechne\\yolov5-master\\yolov5-master')
    img_dir = base_dir / 'runs' / 'detect' / 'images'
    txt_dir = base_dir / 'runs' / 'detect' / 'texts'

    clear_directory(img_dir)
    clear_directory(txt_dir)

    python_executable = base_dir / 'venv' / 'Scripts' / 'python.exe'
    command = [
        str(python_executable),
        str(base_dir / 'detect.py'),
        '--weights', 'best.pt',
        '--source', str(base_dir / 'source')
    ]
    subprocess.run(command)

    # 'seat.txt' 파일의 경로
    file_seat = 'seat.txt'

    # txt_dir 내의 모든 텍스트 파일에 대해 반복
    for file_path in txt_dir.glob('*.txt'):
        matches = match_boxes(file_path, file_seat)
        print(f"Matches for {file_path.name}: {matches}")

run_yolov5_detection()

subprocess.run(['python', 'move.py'])

