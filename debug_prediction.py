#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
예측 결과 상세 분석 스크립트
"""
import os
import sys
import numpy as np
from PIL import Image

# 테스트 이미지 경로 입력
if len(sys.argv) < 2:
    print("사용법: python debug_prediction.py <이미지_경로>")
    print("예시: python debug_prediction.py test_image.jpg")
    sys.exit(1)

image_path = sys.argv[1]

if not os.path.exists(image_path):
    print(f"❌ 이미지를 찾을 수 없습니다: {image_path}")
    sys.exit(1)

print("=" * 70)
print("예측 결과 상세 분석")
print("=" * 70)

# 모델 로드
from model.detect_damage import model, label_classes, device, transform
import torch

# 이미지 로드 및 전처리
print(f"\n이미지: {image_path}")
img = Image.open(image_path).convert("RGB")
print(f"원본 크기: {img.size}")

img_tensor = transform(img).unsqueeze(0).to(device)
print(f"전처리 후 shape: {img_tensor.shape}")

# 예측
with torch.no_grad():
    predictions = model(img_tensor)

predictions = predictions.cpu().numpy()[0]

print("\n" + "=" * 70)
print("전체 클래스별 예측 확률 (상위 10개)")
print("=" * 70)

# 확률 순으로 정렬
sorted_indices = np.argsort(predictions)[::-1]

for i, idx in enumerate(sorted_indices[:10]):
    class_name = label_classes[idx]
    probability = predictions[idx]
    print(f"{i+1:2d}. {class_name:25s} : {probability:.4f} ({probability*100:.2f}%)")

print("\n" + "=" * 70)
print("Front 관련 클래스")
print("=" * 70)

front_classes = [i for i, name in enumerate(label_classes) if 'Front' in name or 'Bonnet' in name or 'Head' in name or 'Windshield' in name]
for idx in front_classes:
    class_name = label_classes[idx]
    probability = predictions[idx]
    marker = "⭐" if probability >= 0.2 else "  "
    print(f"{marker} {class_name:25s} : {probability:.4f} ({probability*100:.2f}%)")

print("\n" + "=" * 70)
print("Rear 관련 클래스")
print("=" * 70)

rear_classes = [i for i, name in enumerate(label_classes) if 'Rear' in name or 'Trunk' in name]
for idx in rear_classes:
    class_name = label_classes[idx]
    probability = predictions[idx]
    marker = "⭐" if probability >= 0.2 else "  "
    print(f"{marker} {class_name:25s} : {probability:.4f} ({probability*100:.2f}%)")

print("\n" + "=" * 70)
print("임계값 0.2 이상인 클래스")
print("=" * 70)

high_prob_indices = np.where(predictions >= 0.2)[0]
if len(high_prob_indices) == 0:
    print("없음")
else:
    for idx in high_prob_indices:
        class_name = label_classes[idx]
        probability = predictions[idx]
        print(f"✓ {class_name:25s} : {probability:.4f} ({probability*100:.2f}%)")

print("\n" + "=" * 70)
