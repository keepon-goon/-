import json
import tempfile
from . import teacher_bp
from flask import Flask, render_template, send_from_directory, request, jsonify
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import requests

client = MongoClient('mongodb://localhost:27017/')
db = client['education']

# 配置上传目录和允许的文件类型
UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'docx', 'pdf', 'txt'}

# 上一次上传的文件名称
last_file_name = ''

API_URL = "https://spark-api-open.xf-yun.com/v2/chat/completions"  # 替换为实际API地址
API_PASSWORD = "SzBawvfnyoiWpTrtDaYq:JfGdQyYBtAtcvdUullJh"  # 替换为实际API密钥

# 敏感词过滤
SENSITIVE_WORDS = ["非法", "敏感"]


@teacher_bp.route('/lessonPrepare')
def lessonPrepare():
    return render_template('teacherPrepare.html')


@teacher_bp.route('/teacherExam')
def teacherExam():
    return render_template('teacherExam.html')


@teacher_bp.route('/teacherAnalyse')
def teacherAnalyse():
    return render_template('teacherAnalyse.html')


# 学生教师管理共用同一个系统管理页面
@teacher_bp.route('/systemAdministration')
def systemAdministration():
    return render_template('systemAdministration.html')


@teacher_bp.route('/upload', methods=['POST'])
def upload_file():
    # 检查请求中是否有文件部分
    if 'file' not in request.files:
        return jsonify({'error': '文件未上传'}), 400

    file = request.files['file']

    # 检查文件是否是允许的类型
    if not allowed_file(file.filename):
        return jsonify(
            {'error': '文件类型不支持，仅支持 .docx, .pdf, .txt'}), 400

    # 安全处理文件名
    filename = secure_filename(file.filename)
    last_file_name = file.filename

    # 使用 tempfile 模块创建临时文件
    with tempfile.NamedTemporaryFile(delete=False,
                                     suffix=os.path.splitext(filename)[
                                         1]) as temp_file:
        temp_path = temp_file.name
        file.save(temp_path)

    # 根据文件类型提取文本内容
    file_texts = ''
    if filename == 'txt':
        with open(temp_path, 'r', encoding='utf-8') as f:
            file_texts = f.read()
            print(file_texts)
    elif filename == 'docx':
        pass
    elif filename == 'pdf':
        pass
    elif filename == 'pptx':
        pass

    # 清理临时文件
    os.remove(temp_path)

    # 将文件信息保存到数据库
    file_data = {
        'filename': file.filename,
        'upload_time': datetime.now(),
        'file_texts': file_texts
    }
    db.uploaded_files.insert_one(file_data)

    # 返回成功响应
    return jsonify({
        'success': True,
        'filename': filename,
        'message': '文件上传成功'
    }), 200


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[
        1].lower() in ALLOWED_EXTENSIONS


@teacher_bp.route('/parseResult')
def parseResult():
    # 从请求参数中获取选中的模型
    model_name = request.args.get('model', 'deepseek-r1')  # 默认使用 deepseek-r1
    if model_name == 'spark':
        try:
            # 获取用户输入
            prompt = db['uploaded_files'].find_one({'filename':'训练数据.txt'})['file_texts']

            # 准备请求
            headers = {
                "Authorization": f"Bearer {API_PASSWORD}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "x1",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "max_tokens": 4096
            }
            print('准备发送请求')
            # 发送请求到API
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()  # 检查请求是否成功

            # 解析响应
            result = response.json()
            content = result["choices"][0]["message"].get("content", "")

            if not content:
                return jsonify({
                    'success': False,
                    'error': 'API返回空内容'
                }), 500

            return jsonify({
                'success': True,
                'content': content
            }), 200
            print(content)

        except requests.exceptions.HTTPError as e:
            return jsonify({
                'success': False,
                'error': f'API请求失败: {str(e)}'
            }), 500

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'处理请求时发生错误: {str(e)}'
            }), 500
    elif model_name == 'deepseek-r1':
        url = "http://localhost:11434/api/generate"
        # 获取用户输入
        prompt = '你好'
        payload = {
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False  # 获取完整响应
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        # 处理 x-ndjson 格式（最后一行包含完整结果）
        lines = response.text.strip().split('\n')
        for line in lines:
            if line.strip():
                data = json.loads(line)
                if data.get("done", False):
                    return jsonify({
                        'success': True,
                        'content': data.get("response", "")
                    }), 200

    elif model_name == 'qwen3':
        pass