import tensorflow as tf
from tensorflow.keras.models import model_from_json
import h5py

old_path = "model/damage_model.h5"
new_path = "model/damage_model_CONVERTED.keras"

try:
    print("[INFO] 구버전 모델 강제 로드 시도 중...")

    # .keras 파일을 HDF5처럼 열어 내부 구조 추출
    with h5py.File(old_path, 'r') as f:
        if 'model_config' in f.attrs:
            json_config = f.attrs['model_config']
            model = model_from_json(json_config)
            model.load_weights(f)
        else:
            raise ValueError("이 파일은 HDF5 기반 Keras 모델이 아닙니다.")

    print("[INFO] 구버전 모델 로드 성공 ✅")
    model.save(new_path)
    print(f"[INFO] 새 모델 저장 완료 ✅ -> {new_path}")

except Exception as e:
    print(f"[ERROR] 변환 실패: {e}")
