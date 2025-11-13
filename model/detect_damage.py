# -*- coding: utf-8 -*-
import os
import json
import numpy as np
import tensorflow as tf
from PIL import Image

# ==============================
# 1️⃣ 설정 및 파일 경로
# ==============================
IMAGE_SIZE = (224, 224)
MODEL_PATH = os.path.join('model', 'damage_model_REBUILT.keras')  # 재구성된 모델 사용
CLASSES_PATH = os.path.join('model', 'class_names (1).json')
PREDICTION_THRESHOLD = 0.2 

# 모델과 클래스 변수를 전역으로 선언 (Flask 앱에서 사용하기 위함)
model = None
label_classes = None

# ==============================
# 2️⃣ 모델 및 클래스 로드
# ==============================
print("🚀 모델 및 클래스 로드 중...")

try:
    # 1. 모델 파일 로드
    from keras.models import load_model
    from keras.applications.efficientnet import preprocess_input
    
    model = load_model(MODEL_PATH, compile=False)
    print(f"✅ 모델 로드 성공: {MODEL_PATH}")
    print(f"   입력 shape: {model.input_shape}")
    print(f"   출력 shape: {model.output_shape}")
    
    # 2. JSON 클래스 파일 로드 및 NumPy 배열로 변환
    with open(CLASSES_PATH, "r", encoding="utf-8") as f:
        label_classes = np.array(json.load(f))
    print(f"✅ 클래스 이름 로드 성공. 총 {len(label_classes)}개 클래스.")

except Exception as e:
    print(f"❌ 파일 로드 중 오류 발생: {e}")
    print("경로 설정을 확인하거나 라이브러리 버전을 확인하십시오.")
    raise SystemExit("모델 또는 클래스 파일 로드 실패")


# ==============================
# 3️⃣ 이미지 전처리 함수
# ==============================
def preprocess_image(image_path):
    """
    이미지 경로를 받아 모델 입력 형식으로 전처리합니다.
    """
    try:
        from keras.applications.efficientnet import preprocess_input
        
        img = Image.open(image_path).convert("RGB")
        img = img.resize(IMAGE_SIZE)
        img_array = np.array(img, dtype=np.float32)
        
        # EfficientNet 전처리
        processed_img = preprocess_input(img_array)
        
        # 배치 차원 추가
        processed_img = np.expand_dims(processed_img, axis=0)
        return processed_img
        
    except FileNotFoundError:
        print(f"❌ 오류: 지정된 이미지 파일이 존재하지 않습니다: {image_path}")
        return None
    except Exception as e:
        print(f"❌ 오류: 이미지 처리 중 예상치 못한 오류 발생: {e}")
        return None

# ==============================
# 4️⃣ 추론 및 결과 해독 함수
# ==============================
def predict_damage(image_path, result_folder):
    """
    Flask 앱과 연동하기 위한 예측 함수
    """
    processed_image = preprocess_image(image_path)
    
    if processed_image is None:
        return None, []

    # 모델 예측
    predictions = model.predict(processed_image)[0]
    
    # 임계값을 넘는 예측값 필터링
    is_predicted = predictions >= PREDICTION_THRESHOLD
    
    predicted_labels = label_classes[is_predicted]
    predicted_probabilities = predictions[is_predicted]
    
    damage_info = []
    
    if len(predicted_labels) == 0:
        damage_info.append({
            "class_name": f"예측 임계값 ({PREDICTION_THRESHOLD})을 넘는 라벨이 없습니다.",
            "probability": ""
        })
    else:
        for label, probability in zip(predicted_labels, predicted_probabilities):
            damage_info.append({
                "class_name": label,
                "probability": f"{probability:.2%}"
            })

    # 원본 이미지를 결과 폴더에 저장
    try:
        os.makedirs(result_folder, exist_ok=True)
        
        original_img = Image.open(image_path)
        result_filename = f"result_{os.path.basename(image_path)}"
        result_path = os.path.join(result_folder, result_filename)
        original_img.save(result_path)
        
    except Exception as e:
        print(f"❌ 오류: 결과 이미지 저장 중 오류 발생: {e}")
        result_path = image_path

    return result_path, damage_info