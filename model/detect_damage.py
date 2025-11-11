# # -*- coding: utf-8 -*-
# import os
# import json
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.models import load_model
# from tensorflow.keras.applications.efficientnet import preprocess_input
# from PIL import Image
# import json
# # ==============================
# # 1️⃣ 설정 및 파일 경로
# # ==============================
# IMAGE_SIZE = (224, 224)
# MODEL_PATH = os.path.join('model', 'new_model_keras215.h5') # 경로 수정
# CLASSES_PATH = os.path.join('model', 'class_names (1).json') # 경로 수정
# PREDICTION_THRESHOLD = 0.2 

# # ==============================
# # 2️⃣ 모델 및 클래스 로드
# # ==============================

# try:
#     # 1. 모델 파일 로드
#     # (참고: 이전 'batch_shape' 오류 방지를 위해 compile=False 추가)
#     model = load_model(MODEL_PATH, compile=False) 
    
#     # 2. JSON 클래스 파일 로드 (❌ load_model(CLASSES_PATH)가 아님)
#     with open(CLASSES_PATH, "r", encoding="utf-8") as f:
#         label_classes = json.load(f)

# except Exception as e:
#     print(f"❌ 파일 로드 중 오류 발생: {e}")

# # ==============================
# # 3️⃣ 이미지 전처리 함수
# # ==============================
# def preprocess_image(image_path):
#     """
#     이미지 경로를 받아 모델 입력 형식으로 전처리합니다.
#     """
#     try:
#         img = Image.open(image_path).convert("RGB")
#         img = img.resize(IMAGE_SIZE)
#         img_array = np.array(img, dtype=np.float32)
#         processed_img = preprocess_input(img_array)
#         processed_img = np.expand_dims(processed_img, axis=0)
#         return processed_img
#     except Exception as e:
#         print(f"❌ 오류: 이미지 처리 중 예상치 못한 오류 발생: {e}")
#         return None

# # ==============================
# # 4️⃣ 추론 및 결과 해독 함수
# # ==============================
# def predict_damage(image_path, result_folder):
#     """
#     Flask 앱과 연동하기 위한 예측 함수
#     """
#     processed_image = preprocess_image(image_path)
    
#     if processed_image is None:
#         return None, []

#     # 모델 예측
#     predictions = model.predict(processed_image)[0]
#     is_predicted = predictions >= PREDICTION_THRESHOLD
#     predicted_labels = label_classes[is_predicted]
    
#     damage_info = []
#     if len(predicted_labels) == 0:
#         damage_info.append({
#             "class_name": f"예측 임계값 ({PREDICTION_THRESHOLD})을 넘는 라벨이 없습니다.",
#             "probability": ""
#         })
#     else:
#         for label in predicted_labels:
#             prob_index = np.where(label_classes == label)[0][0]
#             probability = predictions[prob_index]
#             damage_info.append({
#                 "class_name": label,
#                 "probability": f"{probability:.2%}"
#             })

#     # 원본 이미지를 결과 폴더에 저장 (시각화 로직은 일단 제거)
#     try:
#         original_img = Image.open(image_path)
#         result_filename = f"result_{os.path.basename(image_path)}"
#         result_path = os.path.join(result_folder, result_filename)
#         original_img.save(result_path)
#     except Exception as e:
#         print(f"❌ 오류: 결과 이미지 저장 중 오류 발생: {e}")
#         # 오류 발생 시 원본 이미지 경로라도 반환
#         result_path = image_path

#     return result_path, damage_info

# -*- coding: utf-8 -*-
import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input
from PIL import Image

# ==============================
# 1️⃣ 설정 및 파일 경로
# ==============================
IMAGE_SIZE = (224, 224)
# Flask 앱의 루트 디렉토리 기준으로 'model/new_model_keras215.h5' 경로 설정
MODEL_PATH = os.path.join('model', 'damage_model_FIXED.keras')
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
    # 💡 수정 1: 'batch_shape' 오류 방지를 위해 compile=False 유지
    model = load_model(MODEL_PATH, compile=False) 
    print(f"✅ 모델 로드 성공: {MODEL_PATH}")
    
    # 2. JSON 클래스 파일 로드 및 NumPy 배열로 변환
    with open(CLASSES_PATH, "r", encoding="utf-8") as f:
        # 💡 수정 2: 리스트 인덱싱 오류 방지를 위해 NumPy 배열로 변환
        label_classes = np.array(json.load(f))
    print(f"✅ 클래스 이름 로드 성공. 총 {len(label_classes)}개 클래스.")

except Exception as e:
    print(f"❌ 파일 로드 중 오류 발생: {e}")
    print("경로 설정을 확인하거나 라이브러리 버전을 확인하십시오.")
    # Flask 앱 실행을 중단하여 모델 로드 실패를 알림
    raise SystemExit("모델 또는 클래스 파일 로드 실패")


# ==============================
# 3️⃣ 이미지 전처리 함수
# ==============================
def preprocess_image(image_path):
    """
    이미지 경로를 받아 모델 입력 형식으로 전처리합니다.
    """
    try:
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
    # predictions는 (num_classes,) 형태의 확률 배열
    predictions = model.predict(processed_image)[0]
    
    # 임계값을 넘는 예측값 필터링
    is_predicted = predictions >= PREDICTION_THRESHOLD
    
    # 💡 수정 3: NumPy 인덱싱을 사용하여 라벨과 확률을 효율적으로 추출
    predicted_labels = label_classes[is_predicted]
    predicted_probabilities = predictions[is_predicted]
    
    damage_info = []
    
    if len(predicted_labels) == 0:
        damage_info.append({
            "class_name": f"예측 임계값 ({PREDICTION_THRESHOLD})을 넘는 라벨이 없습니다.",
            "probability": ""
        })
    else:
        # 라벨과 확률을 묶어서 damage_info 리스트 생성
        for label, probability in zip(predicted_labels, predicted_probabilities):
            damage_info.append({
                "class_name": label,
                "probability": f"{probability:.2%}" # 예: 95.23%
            })

    # 원본 이미지를 결과 폴더에 저장
    try:
        # 결과 폴더가 없으면 생성
        os.makedirs(result_folder, exist_ok=True)
        
        original_img = Image.open(image_path)
        result_filename = f"result_{os.path.basename(image_path)}"
        result_path = os.path.join(result_folder, result_filename)
        original_img.save(result_path)
        
    except Exception as e:
        print(f"❌ 오류: 결과 이미지 저장 중 오류 발생: {e}")
        # 오류 발생 시 원본 이미지 경로라도 반환
        result_path = image_path

    return result_path, damage_info