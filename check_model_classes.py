#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모델 파일에서 클래스 정보 추출
"""
import torch
import json

model_path = "model/damage_model_best (1).pth"

print("=" * 70)
print("모델 파일 분석")
print("=" * 70)

checkpoint = torch.load(model_path, map_location='cpu')

print(f"\n체크포인트 타입: {type(checkpoint)}")

if isinstance(checkpoint, dict):
    print(f"\n체크포인트 키:")
    for key in checkpoint.keys():
        print(f"  - {key}")
    
    # 클래스 이름이 저장되어 있는지 확인
    if 'class_names' in checkpoint:
        print(f"\n✅ 모델에 저장된 클래스 이름:")
        class_names = checkpoint['class_names']
        for i, name in enumerate(class_names):
            print(f"  {i:2d}. {name}")
    
    if 'classes' in checkpoint:
        print(f"\n✅ 모델에 저장된 클래스:")
        classes = checkpoint['classes']
        for i, name in enumerate(classes):
            print(f"  {i:2d}. {name}")
    
    # 메타데이터 확인
    if 'metadata' in checkpoint:
        print(f"\n메타데이터:")
        print(json.dumps(checkpoint['metadata'], indent=2, ensure_ascii=False))
    
    # 학습 정보
    if 'epoch' in checkpoint:
        print(f"\n학습 에포크: {checkpoint['epoch']}")
    
    if 'best_acc' in checkpoint or 'best_accuracy' in checkpoint:
        acc = checkpoint.get('best_acc', checkpoint.get('best_accuracy'))
        print(f"최고 정확도: {acc:.4f}")
    
    if 'train_acc' in checkpoint:
        print(f"학습 정확도: {checkpoint['train_acc']:.4f}")
    
    if 'val_acc' in checkpoint:
        print(f"검증 정확도: {checkpoint['val_acc']:.4f}")

else:
    print("\n체크포인트가 state_dict만 포함하고 있습니다.")
    print("클래스 정보가 모델 파일에 저장되지 않았습니다.")

print("\n" + "=" * 70)
print("현재 사용 중인 class_names (1).json:")
print("=" * 70)

with open("model/class_names (1).json", "r", encoding="utf-8") as f:
    current_classes = json.load(f)

for i, name in enumerate(current_classes):
    print(f"  {i:2d}. {name}")

print("\n" + "=" * 70)
