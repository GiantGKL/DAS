from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
import os
import uuid
import cv2
import numpy as np
from data_augmentation import DataAugmentation
import base64
from io import BytesIO

app = Flask(__name__)

# 配置
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# 确保文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 初始化数据增强器
augmenter = DataAugmentation()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_to_base64(image_path):
    """将图像转换为base64编码"""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'files' not in request.files:
            return jsonify({'error': '没有文件被上传'}), 400

        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return jsonify({'error': '没有选择文件'}), 400

        uploaded_files = []
        for file in files:
            if file and allowed_file(file.filename):
                # 生成唯一文件名
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                uploaded_files.append({
                    'filename': unique_filename,
                    'original_name': filename
                })
            else:
                return jsonify({'error': f'不支持的文件格式: {file.filename}'}), 400

        return jsonify({
            'success': True,
            'files': uploaded_files,
            'message': f'成功上传 {len(uploaded_files)} 个文件'
        })

    except Exception as e:
        return jsonify({'error': f'上传失败: {str(e)}'}), 500

@app.route('/augment', methods=['POST'])
def augment_image():
    try:
        data = request.get_json()
        filenames = data.get('filenames', [])
        augmentations = data.get('augmentations', [])

        # 获取参数
        brightness = data.get('brightness', 1.0)
        contrast = data.get('contrast', 1.0)

        if not filenames:
            return jsonify({'error': '没有指定文件名'}), 400

        results = []
        for filename in filenames:
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(input_path):
                results.append({
                    'success': False,
                    'filename': filename,
                    'error': '文件不存在'
                })
                continue

            # 生成输出文件名
            output_filename = f"augmented_{uuid.uuid4()}_{filename}"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

            # 读取图像
            image = cv2.imread(input_path)
            if image is None:
                results.append({
                    'success': False,
                    'filename': filename,
                    'error': '无法读取图像文件'
                })
                continue

            # 应用数据增强，传递参数
            params = {
                'brightness': brightness,
                'contrast': contrast,
                'noise_type': 'gaussian',
                'blur_type': 'gaussian'
            }

            augmented_image = augmenter.apply_augmentation(image, augmentations, **params)

            # 保存结果
            cv2.imwrite(output_path, augmented_image)

            # 将图像转换为base64以便在前端显示
            image_base64 = image_to_base64(output_path)

            results.append({
                'success': True,
                'original_filename': filename,
                'output_filename': output_filename,
                'image_data': f"data:image/jpeg;base64,{image_base64}"
            })

        return jsonify({
            'success': True,
            'results': results,
            'message': f'成功处理 {len([r for r in results if r["success"]])} 个文件'
        })

    except Exception as e:
        return jsonify({'error': f'处理失败: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': '文件不存在'}), 404
    except Exception as e:
        return jsonify({'error': f'下载失败: {str(e)}'}), 500

@app.route('/preview/<filename>')
def preview_original(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            image_base64 = image_to_base64(file_path)
            return jsonify({
                'success': True,
                'image_data': f"data:image/jpeg;base64,{image_base64}"
            })
        else:
            return jsonify({'error': '文件不存在'}), 404
    except Exception as e:
        return jsonify({'error': f'预览失败: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)