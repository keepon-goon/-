from flask import Blueprint, render_template, session, redirect, url_for,request
from flask import Flask, render_template, send_from_directory
from pymongo import MongoClient
from . import auth_bp



client = MongoClient('mongodb://localhost:27017/')
db = client['education']

@auth_bp.route('/')
def home():
    return render_template('login.html')

@auth_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('F:/code/lastTry/pythonProject2/uploads', filename)


@auth_bp.route('/login',methods=['GET','POST'])
def login_to_which():
    if request.method == 'POST':
        #获取表单数据
        role = request.form.get('role')
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')

        collection = db['educationUser']
        #校验账号
        if action == '登录' and collection.find_one({'username':username})['password'] == password:
            session['username'] = username
            session['role'] = role
            if role == '教师':
                return redirect(url_for('auth.teacherSumPage'))
            if role == '学生':
                return redirect(url_for('auth.studentSumPage'))
            if role == '管理':
                return redirect(url_for('auth.managerSumPage'))
        elif action == '登录':
            return '账号密码不匹配或身份选择错误，请重试',400
        if action == '注册' :
            user_data ={
                'username':username,
                'password':password,
                'email':username,
                'roles':role,
            }
            results = collection.insert_one(user_data)
            return '注册成功，请回到上一页面进行登录'

        #GET请求返回登录页面
        return render_template('login.html')

@auth_bp.route('/teacherSumPage')
def teacherSumPage():
    return render_template('teacherSumPage.html')

@auth_bp.route('/studentSumPage')
def studentSumPage():
    return render_template('studentSumPage.html')

@auth_bp.route('/managerSumPage')
def managerSumPage():
    return render_template('managerSumPage.html')








