from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from model.detect_damage import predict_damage

app = Flask(__name__)

# 폴더 설정
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'

# 업로드 및 결과 폴더 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # 모델 예측 (결과 이미지 경로, 손상 부위 리스트 반환)
    result_path, damage_info = predict_damage(filepath, app.config['RESULT_FOLDER'])
    
    return render_template('result.html',
                           result_img=result_path,
                           damage_info=damage_info)

if __name__ == '__main__':
    app.run(debug=True)
