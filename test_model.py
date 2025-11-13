#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyTorch 모델 로드 테스트
"""
import os
import sys

print("=" * 70)
print("PyTorch 모델 로드 테스트")
print("=" * 70)

# 1. PyTorch 버전 확인
try:
    import torch
    print(f"\n✅ PyTorch 버전: {torch.__version__}")
    print(f"   CUDA 사용 가능: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"   CUDA 버전: {torch.version.cuda}")
except ImportError as e:
    print(f"\n❌ PyTorch를 찾을 수 없습니다: {e}")
    print("   pip install torch torchvision 명령어로 설치하세요.")
    sys.exit(1)

# 2. 모델 파일 확인
model_path = "model/damage_model_best (1).pth"
if not os.path.exists(model_path):
    print(f"\n❌ 모델 파일을 찾을 수 없습니다: {model_path}")
    sys.exit(1)

print(f"\n✅ 모델 파일 존재: {model_path}")
file_size = os.path.getsize(model_path)
print(f"   파일 크기: {file_size:,} bytes ({file_size / (1024*1024):.2f} MB)")

# 3. 모델 로드 시도
print("\n" + "=" * 70)
print("모델 로드 시도")
print("=" * 70)

try:
    from model.detect_damage import model, label_classes, device
    
    print(f"\n✅ 모델 로드 성공!")
    print(f"   디바이스: {device}")
    print(f"   클래스 수: {len(label_classes)}개")
    print(f"   모델 파라미터 수: {sum(p.numel() for p in model.parameters()):,}")
    
    # 샘플 입력으로 테스트
    print("\n" + "=" * 70)
    print("샘플 입력 테스트")
    print("=" * 70)
    
    import torch
    sample_input = torch.randn(1, 3, 224, 224).to(device)
    
    with torch.no_grad():
        output = model(sample_input)
    
    print(f"\n✅ 추론 성공!")
    print(f"   입력 shape: {sample_input.shape}")
    print(f"   출력 shape: {output.shape}")
    print(f"   출력 범위: [{output.min():.4f}, {output.max():.4f}]")
    
    print("\n" + "=" * 70)
    print("✅ 모든 테스트 통과!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ 모델 로드 실패: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
