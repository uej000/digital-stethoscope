import os

def find_matching_files(folder_path):
    # 조건 설정
    target_sex = "Male"
    min_height, max_height = 170, 180
    min_weight, max_weight = 60, 80

    # 폴더 내 파일 탐색
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.readlines()
                
                # 변수 초기화
                sex, height, weight = None, None, None
                
                # 내용 읽기
                for line in content:
                    if line.startswith("#Sex:"):
                        sex = line.split(":")[1].strip()
                    elif line.startswith("#Height:"):
                        height = float(line.split(":")[1].strip())
                    elif line.startswith("#Weight:"):
                        weight = float(line.split(":")[1].strip())
                
                # 조건 검사
                if (
                    sex == target_sex and
                    height and min_height <= height <= max_height and
                    weight and min_weight <= weight <= max_weight
                ):
                    print(f"파일: {file_name} | Sex: {sex}, Height: {height}, Weight: {weight}")

# 경로 지정
folder_path = "the-circor-digiscope-phonocardiogram-dataset-1.0.3/training_data"
find_matching_files(folder_path)