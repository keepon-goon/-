from flask import Flask, render_template, request, jsonify, send_file
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
TEXT_DATA_FILE = 'user_text_data.txt'


def save_text_to_file(text, image_filename):
    '''
    保存用户输入的文本到文件中
    '''
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(TEXT_DATA_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] [{image_filename}] {text}\n")


def read_saved_texts():
    '''
    从文件读取所有保存的文本
    :return所有保存的文本的行的列表
    '''
    with open(TEXT_DATA_FILE, 'r', encoding='utf-8') as f:
        return f.readlines()


def get_image_list():
    '''
    获取要上传的图片列表
    '''
    return os.listdir(UPLOAD_FOLDER)  # listdir返回指定目录中所有文件和子目录名称的字符串列表,
    # 仅返回名称，不含路径


# 路由装饰器，用于将一个函数绑定到特定的 URL 路径
@app.route('/')
def index():
    '''
    进行图片索引计算
    '''
    images = get_image_list()
    # 从HTTP请求的URL参数里获取图片索引值，并将其转换为整数类型
    current_image_index = int(request.args.get('index', 0))
    current_image = images[current_image_index]  # 当前图片文件名
    # 实现图片的切换
    if current_image_index + 1 >= len(images):
        next_index = 0
    else:
        next_index = current_image_index + 1
    if current_image_index - 1 < 0:
        prev_index = len(images) - 1  # 第一张图片的上一张是最后一张
    else:
        prev_index = current_image_index - 1

    return render_template('index.html',
                           has_images=True,
                           current_image=current_image,
                           current_image_index=current_image_index,
                           next_index=next_index,
                           prev_index=prev_index,
                           total_images=len(images))


@app.route('/uploads/<filename>')#<filename>是一个路径变量（Path Variable），
#会捕获请求URL中对应位置的字符串，并将其作为参数传递给视图函数
def serve_uploaded_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))
    #Flask调用send_file,读取文件并返回给客户端Flask 调用 send_file,读取文件并返回给客户端


@app.route('/save_text', methods=['POST'])
def save_text():
    data = request.json
    save_text_to_file(data['text'], data['image_filename'])
    return jsonify({#将Python对象转为JSON字符串并返回给客户端
        "message": "文本保存成功",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


if __name__ == '__main__':
    app.run()
