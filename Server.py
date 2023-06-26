#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Server.py
@Time    :   2023/06/17 19:12:16
@Author  :   CryMang 
@Version :   1.0
@Contact :   uamind@foxmail.com
@License :   GPL v3.0 (https://www.gnu.org/licenses/gpl-3.0.html)
@Description :
该软件受GNU通用公共许可证（GPL）保护。
如果您使用本软件，则必须符合GPL下的条款，
可以在以下位置查看完整许可证文本：
    https://www.gnu.org/licenses/gpl-3.0.html
或者通过向Free Software Foundation, Inc.发送请求获得。
'''

# Here put the import libraries
# 导入 Flask 应用及相关模块
from flask import Flask, request, jsonify
import json

# 创建 Flask 应用实例
app = Flask(__name__)

#禁止ASCII码
app.config['JSON_AS_ASCII'] = False

# 指定浏览器渲染的文件类型，和解码格式
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"  

# 初始化学生列表
students = [
    {'id': 1, '名字': '张三', '年龄': 18},
    {'id': 2, '名字': '李四', '年龄': 19},
    {'id': 3, '名字': '王五', '年龄': 20},
]

# 主页路由
@app.route('/')
def home():
    # 生成包含所有学生信息的 HTML 表格
    table_html = '<table><thead><tr><th>ID</th><th>名字</th><th>年龄</th></tr></thead><tbody>'
    for student in students:
        table_html += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(student['id'], student['名字'], student['年龄'])
    table_html += '</tbody></table>'

    # 返回包含学生信息的页面
    return '''
        <html>
            <head>
                <title>Student list</title>
            </head>
            <body>
                <h1>Student list</h1>
                {}
            </body>
        </html>
    '''.format(table_html)

# 处理获取学生信息的函数
@app.route('/students', methods=['GET'])
def get_students():
    global students
    student_id = request.args.get('id')
    filtered_students = []

    # 根据学生 ID 进行筛选
    if student_id:
        for student in students:
            if student['id'] == int(student_id):
                filtered_students.append(student)
    else:
        filtered_students = students

    # 返回筛选后的学生信息（JSON 格式）
    data = filtered_students
    sjson = json.dumps(data,ensure_ascii=False).encode('utf-8')
    return sjson

# 处理添加学生信息的函数
@app.route('/students', methods=['POST'])
def add_student():
    global students

    new_student = request.get_json()

    # 检查请求格式是否正确
    if not new_student:
        return jsonify({'msg': 'Invalid data format'}), 400
    if not all(key in new_student for key in ('id', '名字', '年龄')):
        return jsonify({'msg': 'Missing required fields'}), 400

    # 检查学生是否已存在
    for student in students:
        if student['id'] == new_student['id']:
            return jsonify({'msg': 'Student with this ID already exists'}), 400

    # 添加新学生到学生列表
    students.append(new_student)

    # 返回添加成功信息
    return jsonify({'msg': 'Student added successfully'})

# 处理删除学生信息的函数
@app.route('/students', methods=['DELETE'])
def delete_student():
    global students

    student_id = request.form.get('id')

    # 检查参数是否存在或者格式是否正确
    if not student_id:
        return jsonify({'msg': 'Missing required fields'}), 400
    try:
        student_id = int(student_id)
    except ValueError:
        return jsonify({'msg': 'Invalid ID format'}), 400

    # 在学生列表中查找要删除的学生
    for i, student in enumerate(students):
        if student['id'] == student_id:
            del students[i]
            return jsonify({'msg': 'Student deleted successfully'})

    # 如果未找到要删除的学生，则返回错误信息
    return jsonify({'msg': 'Student not found'}), 400



# 启动应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)