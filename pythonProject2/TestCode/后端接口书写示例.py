# 从flask模块导入必要的类和函数
# Flask: 创建Web应用实例
# render_template: 渲染HTML模板文件
# request: 处理HTTP请求（如表单、文件、JSON数据）
# jsonify: 将Python字典转换为JSON响应
# send_file: 返回文件内容作为响应
from flask import Flask, render_template, request, jsonify, send_file

# 导入os模块用于操作系统相关功能（如文件路径操作、目录检查）
import os

# 从werkzeug.utils导入secure_filename函数
# 用于安全处理文件名，防止目录遍历攻击（如恶意文件名：../../etc/passwd）
from werkzeug.utils import secure_filename

# 从datetime模块导入datetime类，用于生成时间戳
from datetime import datetime

# 创建Flask应用实例，__name__是Python内置变量，表示当前模块名称
# Flask使用__name__来确定应用的根路径，用于查找模板和静态文件
app = Flask(__name__)

# 定义上传文件的目标文件夹名称
UPLOAD_FOLDER = 'uploads'

# 定义允许上传的文件扩展名集合
# 只允许上传PNG、JPG、JPEG和GIF格式的图片
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 定义存储用户文本数据的文件名
TEXT_DATA_FILE = 'user_text_data.txt'

# 确保上传文件夹存在，如果不存在则创建
# os.path.exists: 检查路径是否存在
# os.makedirs: 创建目录（包括必要的父目录）
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 定义辅助函数：检查文件名是否符合允许的扩展名
# filename: 待检查的文件名（如"example.jpg"）
def allowed_file(filename):
    # 检查文件名是否包含点号（表示有扩展名）
    # 并检查扩展名是否在ALLOWED_EXTENSIONS集合中
    # filename.rsplit('.', 1)[1]: 从右向左分割一次，取扩展名部分
    # .lower(): 将扩展名转为小写，确保大小写不敏感
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 保存用户输入的文本到文件
# text: 用户输入的文本内容
def save_text_to_file(text):
    # 生成当前时间戳，格式为"YYYY-MM-DD HH:MM:SS"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 以追加模式打开文件，并写入文本
    # 'a': 追加模式，文件不存在时会自动创建
    # encoding='utf-8': 指定编码，确保支持中文等特殊字符
    with open(TEXT_DATA_FILE, 'a', encoding='utf-8') as f:
        # 写入格式：[时间戳] 文本内容\n
        f.write(f"[{timestamp}] {text}\n")

# 从文件读取所有保存的文本
# 返回：包含所有文本行的列表
def read_saved_texts():
    # 检查文件是否存在，不存在则返回空列表
    if not os.path.exists(TEXT_DATA_FILE):
        return []

    # 以只读模式打开文件并读取所有行
    with open(TEXT_DATA_FILE, 'r', encoding='utf-8') as f:
        return f.readlines()

# 定义根路由（/），处理GET请求
# 当用户访问网站首页时，执行此函数
@app.route('/')
def index():
    # 初始化空列表，用于存储上传的图片文件名
    uploaded_images = []

    # 检查上传文件夹是否存在（避免首次访问时出错）
    if os.path.exists(UPLOAD_FOLDER):
        # 获取上传文件夹中的所有文件和文件夹
        # os.listdir返回文件名列表（不包含路径）
        all_items = os.listdir(UPLOAD_FOLDER)

        # 过滤出符合条件的文件：
        # 1. 文件名通过allowed_file检查（扩展名允许）
        # 2. 是文件而非目录（os.path.isfile检查）
        # os.path.join: 拼接路径（如"uploads/example.jpg"）
        uploaded_images = [f for f in all_items
                           if allowed_file(f) and os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]

    # 读取已保存的文本数据
    saved_texts = read_saved_texts()

    # 渲染templates目录下的index.html模板
    # 并将uploaded_images和saved_texts列表作为参数传递给模板
    return render_template('index.html', images=uploaded_images, saved_texts=saved_texts)

# 定义文件上传路由，只接受POST请求
@app.route('/upload', methods=['POST'])
def upload_file():
    # 检查请求中是否包含名为'file'的文件字段
    # request.files: 包含所有上传文件的字典
    if 'file' not in request.files:
        # 若不存在，返回错误JSON响应和400状态码
        return jsonify({"error": "没有文件部分"}), 400

    # 从请求中获取上传的文件对象
    file = request.files['file']

    # 检查用户是否选择了文件（空文件名表示未选择）
    if file.filename == '':
        return jsonify({"error": "没有选择文件"}), 400

    # 验证文件是否存在且扩展名允许
    if file and allowed_file(file.filename):
        # 使用secure_filename安全处理文件名
        # 防止恶意文件名（如包含路径分隔符）
        filename = secure_filename(file.filename)

        # 拼接完整的文件保存路径
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # 将上传的文件保存到指定路径
        file.save(file_path)

        # 返回成功JSON响应，包含文件名
        return jsonify({"message": "文件上传成功", "filename": filename})
    else:
        # 若文件类型不允许，返回错误JSON响应
        # ', '.join(ALLOWED_EXTENSIONS): 将允许的扩展名转为字符串
        return jsonify({"error": "不允许的文件类型，仅支持: " + ', '.join(ALLOWED_EXTENSIONS)}), 400

# 定义静态文件服务路由
# <filename>是URL变量，用于指定要访问的文件名
@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    # 从上传文件夹中读取文件并返回
    # send_file: Flask提供的函数，用于发送文件内容
    # os.path.join: 拼接完整文件路径
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

# 定义保存文本的API路由，只接受POST请求
@app.route('/save_text', methods=['POST'])
def save_text():
    # 从POST请求中获取JSON数据
    # request.json: 自动解析请求体中的JSON数据为Python字典
    data = request.json

    # 从字典中提取text字段的值，默认值为空字符串
    # .strip(): 去除字符串首尾的空白字符
    text = data.get('text', '').strip()

    # 检查文本是否为空
    if not text:
        return jsonify({"error": "文本不能为空"}), 400

    # 调用save_text_to_file函数将文本保存到文件
    save_text_to_file(text)

    # 返回成功响应，包含保存的文本和时间戳
    return jsonify({
        "message": "文本保存成功",
        "text": text,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# 定义获取保存文本的API路由，只接受GET请求
@app.route('/get_saved_texts', methods=['GET'])
def get_saved_texts():
    # 调用read_saved_texts函数获取所有保存的文本行
    texts = read_saved_texts()

    # 初始化空列表，用于存储格式化后的文本数据
    formatted_texts = []

    # 遍历每一行文本，解析时间戳和内容
    for line in texts:
        # 按'] '分割字符串，获取时间戳和内容部分
        # 例如："[2023-10-20 14:30:25] 文本内容" → ['[2023-10-20 14:30:25', '文本内容']
        parts = line.strip().split('] ', 1)

        # 确保分割结果包含时间戳和内容两部分
        if len(parts) == 2:
            timestamp, content = parts
            # 将解析结果添加到格式化列表中
            # timestamp[1:]: 去除时间戳开头的'['字符
            formatted_texts.append({
                "timestamp": timestamp[1:],
                "content": content
            })

    # 返回JSON响应，包含格式化的文本列表和总数
    return jsonify({
        "texts": formatted_texts,
        "count": len(formatted_texts)
    })

# 判断当前脚本是否作为主程序运行（而非被其他模块导入）
# __name__是Python内置变量，当脚本直接运行时为'__main__'
if __name__ == '__main__':
    # 启动Flask应用的开发服务器
    # debug=True: 开启调试模式
    #  - 代码修改后自动重启服务器
    #  - 出错时显示详细的错误堆栈信息
    # 注意：生产环境应关闭调试模式，改用WSGI服务器（如Gunicorn、uWSGI）
    app.run(debug=True)