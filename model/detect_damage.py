# -*- coding: utf-8 -*-
import os
import json
import numpy as np
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# ==============================
# 1️⃣ 설정 및 파일 경로
# ==============================
IMAGE_SIZE = (224, 224)
MODEL_PATH = os.path.join('model', 'damage_model_best (3).pth')
CLASSES_PATH = os.path.join('model', 'damage_classes.json')
PREDICTION_THRESHOLD = 0.2

# 디바이스 설정
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 모델과 클래스 변수를 전역으로 선언
model = None
label_classes = None

# ==============================
# 2️⃣ 모델 아키텍처 정의
# ==============================
class DamageClassifier(nn.Module):
    """
    EfficientNet 기반 차량 손상 분류 모델
    """
    def __init__(self, num_classes=32):
        super(DamageClassifier, self).__init__()
        # EfficientNet-B0 백본
        efficientnet = models.efficientnet_b0(pretrained=False)
        self.features = efficientnet.features
        self.avgpool = efficientnet.avgpool
        
        # 분류 레이어
        in_features = 1280  # EfficientNet-B0의 출력 채널 수
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.5),
            nn.Linear(in_features, num_classes),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

# ==============================
# 3️⃣ 이미지 전처리 변환
# ==============================
transform = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ==============================
# 4️⃣ 모델 및 클래스 로드
# ==============================
print("🚀 모델 및 클래스 로드 중...")
print(f"   디바이스: {device}")
print(f"   모델 경로: {MODEL_PATH}")
print(f"   파일 존재 여부: {os.path.exists(MODEL_PATH)}")

try:
    # 1. 클래스 이름 로드
    with open(CLASSES_PATH, "r", encoding="utf-8") as f:
        label_classes = np.array(json.load(f))
    print(f"✅ 클래스 이름 로드 성공. 총 {len(label_classes)}개 클래스.")
    
    # 2. 모델 초기화
    num_classes = len(label_classes)
    model = DamageClassifier(num_classes=num_classes)
    
    # 3. 가중치 로드
    checkpoint = torch.load(MODEL_PATH, map_location=device)
    
    # checkpoint 처리
    if isinstance(checkpoint, dict):
        if 'model_state_dict' in checkpoint:
            state_dict = checkpoint['model_state_dict']
        elif 'state_dict' in checkpoint:
            state_dict = checkpoint['state_dict']
        else:
            state_dict = checkpoint
    else:
        state_dict = checkpoint
    
    # state_dict 로드 (strict=False로 설정하여 일부 키 불일치 허용)
    model.load_state_dict(state_dict, strict=False)
    
    # 4. 모델을 평가 모드로 설정
    model.to(device)
    model.eval()
    
    print(f"✅ 모델 로드 성공!")
    print(f"   입력 크기: {IMAGE_SIZE}")
    print(f"   출력 클래스: {num_classes}개")

except Exception as e:
    print(f"❌ 파일 로드 중 오류 발생: {e}")
    print(f"   오류 타입: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    raise SystemExit("모델 또는 클래스 파일 로드 실패")

# ==============================
# 5️⃣ 이미지 전처리 함수
# ==============================
def preprocess_image(image_path):
    """
    이미지 경로를 받아 모델 입력 형식으로 전처리합니다.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        img_tensor = transform(img)
        img_tensor = img_tensor.unsqueeze(0)
        return img_tensor
        
    except FileNotFoundError:
        print(f"❌ 오류: 지정된 이미지 파일이 존재하지 않습니다: {image_path}")
        return None
    except Exception as e:
        print(f"❌ 오류: 이미지 처리 중 예상치 못한 오류 발생: {e}")
        return None

# ==============================
# 6️⃣ 추론 및 결과 해독 함수
# ==============================
def predict_damage(image_path, result_folder):
    """
    Flask 앱과 연동하기 위한 예측 함수
    """
    processed_image = preprocess_image(image_path)
    
    if processed_image is None:
        return None, []
    
    try:
        processed_image = processed_image.to(device)
        
        with torch.no_grad():
            predictions = model(processed_image)
        
        predictions = predictions.cpu().numpy()[0]
        
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
            sorted_indices = np.argsort(predicted_probabilities)[::-1]
            for idx in sorted_indices:
                label = predicted_labels[idx]
                probability = predicted_probabilities[idx]
                damage_info.append({
                    "class_name": label,
                    "probability": f"{probability:.2%}"
                })
        
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
        
    except Exception as e:
        print(f"❌ 예측 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return None, []
