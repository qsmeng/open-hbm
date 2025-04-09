from backend import app
from flask import jsonify, request
import bcrypt  
import db.hbm_db as hbm_db
import mysql.connector
from datetime import datetime

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # 提取参数并合并到一个字典中
    user_data = {
        'username': data.get('username'),
        'password_hash': bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        'email': data.get('email'),
        'phone_number': data.get('phone_number'),
        'gender': data.get('gender'),
        'birthdate': data.get('birthdate'),
        'country': data.get('country'),  # 新增字段
        'city': data.get('city'),        # 新增字段
        'invite_code': data.get('invite_code'),  # 新增字段
        'is_verified': 0,  # 默认未验证
        'created_at': datetime.now()  # 创建时间
    }

    try:
        user_id = hbm_db.insert_data('user_base_info', user_data)  # 调用 insert_data 方法
        return jsonify({'message': '注册成功！', 'user_id': user_id}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400




@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
