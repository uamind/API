#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   AutoTest.py
@Time    :   2023/06/17 19:16:12
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
# 导入所需的库
import unittest # 单元测试框架
import requests # HTTP请求库

SERVER_URL = 'http://localhost:80'

# 定义测试用例类：TestStudentAPI，继承自unittest.TestCase
class TestStudentAPI(unittest.TestCase):
    
    # 初始化测试环境，添加三个学生数据
    def setUp(self):
        self.students = [
            {'id': 1, '名字': '张三', '年龄': 18},
            {'id': 2, '名字': '李四', '年龄': 19},
            {'id': 3, '名字': '王五', '年龄': 20}
        ]
        # 清空数据
        response = requests.get(SERVER_URL + '/students').json()
        ids = [student['id'] for student in response]
        for id in ids:
            data = {"id" : id}
            requests.delete(SERVER_URL + '/students', data=data)
        # 初始化测试环境，添加三个学生数据
        for student in self.students:
            requests.post(SERVER_URL + '/students', json=student)

    # 测试首页功能是否正常
    def test_home(self):
        print("测试首页")
        response = requests.get(SERVER_URL)
        self.assertEqual(response.status_code, 200) #判断返回的状态码是否为 200
        self.assertIn('<h1>Student list</h1>', response.text) #判断 response.text 中是否包含特定文本
        self.assertIn('<th>ID</th><th>名字</th><th>年龄</th>', response.text) #判断 response.text 中是否包含特定文本

    # 测试获取学生信息功能是否正常
    def test_get_students(self):
        print("测试获取学生信息")
        # 测试 ID 存在时返回数据
        response = requests.get(SERVER_URL + '/students', params={'id': 1})
        self.assertEqual(response.status_code, 200) #判断返回的状态码是否为 200
        self.assertEqual(len(response.json()), 1) #判断返回的数据中是否只有一条记录
        self.assertEqual(response.json()[0]['名字'], '张三') #判断返回的数据中是否包含正确的姓名
        self.assertEqual(response.json()[0]['年龄'], 18) #判断返回的数据中是否包含正确的年龄
        # 测试 ID 不存在时返回空数据
        nonexistent_id = self._get_nonexistent_student_id()
        response = requests.get(SERVER_URL + '/students', params={'id': nonexistent_id})
        self.assertEqual(response.status_code, 200) #判断返回的状态码是否为 200
        self.assertEqual(len(response.json()), 0) #判断返回的数据中是否为空列表
        # 测试未指定 ID 时返回所有数据
        response = requests.get(SERVER_URL + '/students')
        self.assertEqual(response.status_code, 200) #判断返回的状态码是否为 200
        self.assertEqual(len(response.json()), len(self.students)) #判断返回的数据中是否包含了全部的学生记录

    # 测试添加学生信息功能是否正常
    def test_add_student(self):
        print("测试添加学生信息")
        # 测试合法数据
        new_student = {'id': 4, '名字': '赵六', '年龄': 21}
        response = requests.post(SERVER_URL + '/students', json=new_student)
        self.assertEqual(response.status_code, 200) #判断返回的状态码是否为 200
        self.assertEqual(response.json()['msg'], 'Student added successfully') #判断返回的消息是否正确
        self.assertEqual(len(requests.get(SERVER_URL + '/students').json()), 4) #判断添加学生记录成功之后，学生记录总数是否增加
        # 测试非法数据：数据格式不正确
        response = requests.post(SERVER_URL + '/students', json={'invalid': 'data'})
        self.assertEqual(response.status_code, 400) #判断返回的状态码是否为 400
        self.assertEqual(response.json()['msg'], 'Missing required fields') #判断返回的消息是否正确
        # 测试非法数据：缺少必要字段
        response = requests.post(SERVER_URL + '/students', json={'id': 5, '名字': '孙七'})
        self.assertEqual(response.status_code, 400) #判断返回的状态码是否为 400
        self.assertEqual(response.json()['msg'], 'Missing required fields') #判断返回的消息是否正确
        # 测试非法数据：ID 已存在
        response = requests.post(SERVER_URL + '/students', json={'id': 4, '名字': '赵六', '年龄': 22})
        self.assertEqual(response.status_code, 400) #判断返回的状态码是否为 400
        self.assertEqual(response.json()['msg'], 'Student with this ID already exists') #判断返回的消息是否正确

    # 测试删除学生信息功能是否正常
    def test_delete_student(self):
        print("测试删除学生信息")
        # 测试 ID 存在时能够成功删除
        data = {"id" : "1"}
        response = requests.delete(SERVER_URL + '/students', data=data)
        self.assertEqual(response.status_code, 200) #判断返回的状态码是否为 200
        self.assertEqual(response.json()['msg'], 'Student deleted successfully') #判断返回的消息是否正确
        self.assertEqual(len(requests.get(SERVER_URL + '/students').json()), len(self.students) - 1) #判断删除学生记录成功之后，学生记录总数是否减少
        # 测试 ID 不存在时报错
        data = {"id" : "6"}
        response = requests.delete(SERVER_URL + '/students', data=data)
        self.assertEqual(response.status_code, 400) #判断返回的状态码是否为 400
        self.assertEqual(response.json()['msg'], 'Student not found') #判断返回的消息是否正确
        # 测试传递非数字 ID 时是否能够正确返回错误信息
        data = {"id" : "abc"}
        response = requests.delete(SERVER_URL + '/students', data=data)
        self.assertEqual(response.status_code, 400) #判断返回的状态码是否为 400
        self.assertEqual(response.json()['msg'], 'Invalid ID format') #判断返回的消息是否正确
        # 测试未传递 ID 时是否能够正确返回错误信息
        response = requests.delete(SERVER_URL + '/students')
        self.assertEqual(response.status_code, 400) #判断返回的状态码是否为 400
        self.assertEqual(response.json()['msg'], 'Missing required fields') #判断返回的消息是否正确


    # 获取一个不存在的学生ID，在已存在的学生ID中随机选择
    def _get_nonexistent_student_id(self):
        """
        在已存在的学生 ID 中随机选择一个不存在的 ID
        如果所有 ID 都已被占用，则返回 None
        """
        existing_ids = [student['id'] for student in self.students]
        all_ids = set(range(1, len(existing_ids) + 2))
        nonexistent_ids = list(all_ids - set(existing_ids))
        if len(nonexistent_ids) == 0:
            return None
        return nonexistent_ids[0]

# 程序入口
if __name__ == '__main__':
    setup = TestStudentAPI()
    setup.setUp() # 初始化测试环境
    unittest.main() # 运行unittest 测试用例